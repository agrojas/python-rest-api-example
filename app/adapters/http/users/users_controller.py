import logging

from fastapi import Depends, APIRouter
from typing import List

from fastapi.security import OAuth2PasswordBearer
from app.adapters.http.auth.jwt_authenticator import JwtAuthenticator
from app.dependencies.dependencies import (
    jwt_auth_dependency,
    user_usecases_dependency,
)
from app.adapters.http.users.input.user import UserRequest
from app.adapters.http.users.output.user import UserResponse
from app.domain.users.usecases.user_usecases import UserUseCases

router = APIRouter()
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/users/me", response_model=UserResponse)
async def read_users_me(
    token: str = Depends(oauth2_scheme),
    jwt_auth: JwtAuthenticator = Depends(jwt_auth_dependency),
):
    return jwt_auth.authenticate(token)


@router.get('/users', response_model=List[UserResponse])
async def get_users(user_usecases: UserUseCases = Depends(user_usecases_dependency)):
    logger.info("Get all users called")
    return user_usecases.list()


@router.post('/users', response_model=UserResponse)
async def create_users(
    user_request: UserRequest,
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    logger.info("Create user called")
    return user_usecases.register(user_request.to_create_user_command())
