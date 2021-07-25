import logging

from fastapi import Depends, APIRouter, HTTPException, status
from typing import List

from fastapi.security import OAuth2PasswordBearer

from app.adapters.http.auth.exceptions.authentication_exception import (
    AuthenticationException,
)
from app.adapters.http.auth.jwt_authenticator import JwtAuthenticator
from app.dependencies.dependencies import (
    jwt_auth_dependency,
    user_usecases_dependency,
)
from app.adapters.http.users.input.user import UserRequest, UserStatusRequest
from app.adapters.http.users.output.user import UserResponse
from app.domain.users.command.user_update_status_command import UpdateUserStatusCommand
from app.domain.users.usecases.user_usecases import UserUseCases

router = APIRouter()
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/users/me", response_model=UserResponse)
async def read_users_me(
    token: str = Depends(oauth2_scheme),
    jwt_auth: JwtAuthenticator = Depends(jwt_auth_dependency),
):
    try:
        return jwt_auth.authenticate(token)
    except AuthenticationException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get('/users/{user_id}', response_model=UserResponse)
async def get_user(
    user_id: str, user_usecases: UserUseCases = Depends(user_usecases_dependency)
):
    logger.info("Get user by id called")
    user = user_usecases.find_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {user_id} not found',
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


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
    try:
        return user_usecases.register(user_request.to_create_user_command())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.patch('/users/{user_id}/status', response_model=UserResponse)
async def update_status_users(
    user_id: str,
    user_status_request: UserStatusRequest,
    token: str = Depends(oauth2_scheme),
    jwt_auth: JwtAuthenticator = Depends(jwt_auth_dependency),
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    logger.info("Update user status called")
    try:
        jwt_auth.authenticate(token)
        return user_usecases.update_status(
            UpdateUserStatusCommand(user_id, user_status_request.status)
        )
    except AuthenticationException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e,
            headers={"WWW-Authenticate": "Bearer"},
        )
