from functools import lru_cache
from typing import Iterator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.adapters.database.database import get_session_factory
from app.adapters.database.users.sql_user_repository import SQLUserRepository
from app.adapters.database.users.unit_of_work import UserUnitOfWork
from app.adapters.http.auth.authenticator import Authenticator
from app.adapters.http.auth.jwt_user_signer import JwtUserSigner
from app.domain.users.auth.bycryp_password_encoder import ByCryptPasswordEncoder
from app.domain.users.auth.password_encoder import PasswordEncoder
from app.domain.users.repository.unit_of_work import AbstractUserUnitOfWork
from app.domain.users.repository.user_repository import UserRepository
from app.domain.users.usecases.user_authentication_usecases import (
    UserAuthenticationUseCases,
)
from app.domain.users.usecases.user_usecases import UserUseCases
from app.conf.config import Settings
from app.domain.users.model.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")


@lru_cache()
def get_settings():
    return Settings()


def get_session(settings: Settings = Depends(get_settings)) -> Iterator[Session]:
    SessionFactory: Session = get_session_factory(settings)
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


def user_repository_dependency(
    session: Session = Depends(get_session),
) -> UserRepository:
    return SQLUserRepository(session)


def user_uow_dependency(
    session: Session = Depends(get_session),
    user_repository: UserRepository = Depends(user_repository_dependency),
) -> AbstractUserUnitOfWork:
    return UserUnitOfWork(user_repository, session)


def password_encoder_dependency() -> PasswordEncoder:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return ByCryptPasswordEncoder(pwd_context)


def user_auth_usecases_dependency(
    user_uow: AbstractUserUnitOfWork = Depends(user_uow_dependency),
    pwd_encoder: PasswordEncoder = Depends(password_encoder_dependency),
) -> UserAuthenticationUseCases:
    return UserAuthenticationUseCases(user_uow, pwd_encoder)


def user_usecases_dependency(
    user_uow: AbstractUserUnitOfWork = Depends(user_uow_dependency),
    pwd_encoder: PasswordEncoder = Depends(password_encoder_dependency),
) -> UserUseCases:
    return UserUseCases(user_uow, pwd_encoder)


def jwt_auth_dependency(
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
    settings: Settings = Depends(get_settings),
) -> Authenticator:
    return Authenticator(user_usecases, settings)


def jwt_user_signer_dependency(
    settings: Settings = Depends(get_settings),
) -> JwtUserSigner:
    return JwtUserSigner(settings)


def user_token_validation(
    token: str = Depends(oauth2_scheme),
    jwt_auth: Authenticator = Depends(jwt_auth_dependency),
) -> User:
    return jwt_auth.authenticate(token)
