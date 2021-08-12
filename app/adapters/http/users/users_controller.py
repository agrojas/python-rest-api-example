import logging
from typing import List

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.adapters.http.auth.authenticator import Authenticator
from app.adapters.http.auth.exceptions.authentication_exception import (
    AuthenticationException,
)
from app.adapters.http.users.input.user import UserRequest, UserStatusRequest
from app.adapters.http.users.output.user import UserResponse
from app.dependencies.dependencies import (
    jwt_auth_dependency,
    user_usecases_dependency,
)
from app.domain.users.command.user_update_status_command import UpdateUserStatusCommand
from app.domain.users.model.user_exceptions import (
    UsersNotFoundError,
    UserAlreadyHadStatusError,
    UserAlreadyExistException,
)
from app.domain.users.usecases.user_usecases import UserUseCases

router = APIRouter()
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/users/me", response_model=UserResponse)
async def read_users_me(
    token: str = Depends(oauth2_scheme),
    jwt_auth: Authenticator = Depends(jwt_auth_dependency),
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
    user_id: str,
    token: str = Depends(oauth2_scheme),
    jwt_auth: Authenticator = Depends(jwt_auth_dependency),
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    try:
        jwt_auth.authenticate(token)
        logger.info("Get user by id called")
        user = user_usecases.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=UsersNotFoundError(user_id).message,
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except AuthenticationException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get('/users', response_model=List[UserResponse])
async def get_users(
    token: str = Depends(oauth2_scheme),
    jwt_auth: Authenticator = Depends(jwt_auth_dependency),
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    try:
        jwt_auth.authenticate(token)
        logger.info("Get all users called")
        return user_usecases.list()
    except AuthenticationException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post('/users', response_model=UserResponse)
async def create_users(
    user_request: UserRequest,
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    logger.info("Create user called")
    try:
        return user_usecases.register(user_request.to_create_user_command())
    except UserAlreadyExistException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.patch('/users/{user_id}/status', response_model=UserResponse)
async def update_status_users(
    user_id: str,
    user_status_request: UserStatusRequest,
    token: str = Depends(oauth2_scheme),
    jwt_auth: Authenticator = Depends(jwt_auth_dependency),
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    logger.info("Update user status called")
    try:
        jwt_auth.authenticate(token)
        return user_usecases.update_status(
            UpdateUserStatusCommand(user_id=user_id, status=user_status_request.status)
        )
    except AuthenticationException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except UserAlreadyHadStatusError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
