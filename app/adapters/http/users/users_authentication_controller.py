import logging

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.adapters.database.users.in_memory_user_repository import InMemoryUserRepository
from app.adapters.http.auth.jwt_user_signer import JwtUserSigner
from app.adapters.http.auth.output.token import Token
from app.domain.users.command.user_credentials_command import UserCredentialsCommand
from app.domain.users.usecases.user_authentication_usecases import (
    UserAuthenticationUseCases,
)
from app.db import users_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()
logger = logging.getLogger(__name__)
user_repository = InMemoryUserRepository(users_db)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserAuthenticationUseCases(user_repository, pwd_context).find_by_credentials(
        UserCredentialsCommand(form_data.username, form_data.password)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return Token(
        access_token=JwtUserSigner().create_access_token(user.username),
        token_type='bearer',
    )
