import logging
from typing import List

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

from app.adapters.http.auth.authenticator import Authenticator
from app.adapters.http.users.input.user import UserRequest, UserStatusRequest
from app.adapters.http.users.output.user import UserResponse
from app.dependencies.dependencies import (
    jwt_auth_dependency,
    user_usecases_dependency,
)
from app.domain.users.command.user_update_status_command import UpdateUserStatusCommand
from app.domain.users.usecases.user_usecases import UserUseCases

router = APIRouter()
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")


@router.get('/users/{user_id}', response_model=UserResponse)
async def get_user(
    user_id: str,
    token: str = Depends(oauth2_scheme),
    jwt_auth: Authenticator = Depends(jwt_auth_dependency),
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    jwt_auth.authenticate(token)
    logger.info("Get user by id called")
    user = user_usecases.find_by_id(user_id)
    return user


@router.get('/users', response_model=List[UserResponse])
async def get_users(
    token: str = Depends(oauth2_scheme),
    jwt_auth: Authenticator = Depends(jwt_auth_dependency),
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    jwt_auth.authenticate(token)
    logger.info("Get all users called")
    return user_usecases.list()


@router.post('/users', response_model=UserResponse)
async def create_users(
    user_request: UserRequest,
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    logger.info("Create user called")
    return user_usecases.register(user_request.to_create_user_command())


@router.patch('/users/{user_id}/status', response_model=UserResponse)
async def update_status_users(
    user_id: str,
    user_status_request: UserStatusRequest,
    token: str = Depends(oauth2_scheme),
    jwt_auth: Authenticator = Depends(jwt_auth_dependency),
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    logger.info("Update user status called")
    jwt_auth.authenticate(token)
    return user_usecases.update_status(
        UpdateUserStatusCommand(user_id=user_id, status=user_status_request.status)
    )
