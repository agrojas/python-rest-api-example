import logging

from fastapi import Depends, APIRouter
from typing import List

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.adapters.database.users.in_memory_user_repository import InMemoryUserRepository
from app.adapters.http.auth.jwt_authenticator import JwtAuthenticator
from app.adapters.http.users.input.user import UserRequest
from app.adapters.http.users.output.user import UserResponse
from app.domain.users.model.user import User
from app.domain.users.usecases.user_usecases import UserUseCases
from app.db import users_db

router = APIRouter()
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_repository = InMemoryUserRepository(users_db)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_usecases = UserUseCases(user_repository, pwd_context)
jwt_auth = JwtAuthenticator(user_usecases)


@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(jwt_auth.authenticate)):
    return current_user


@router.get('/users', response_model=List[UserResponse])
async def get_users():
    logger.info("Get all users called")
    return user_usecases.list()


@router.post('/users', response_model=UserResponse)
async def create_users(user_request: UserRequest):
    logger.info("Get all users called")
    return user_usecases.register(user_request.to_create_user_command())
