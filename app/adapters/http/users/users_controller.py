import logging
from typing import List

from fastapi import Depends, APIRouter, status

from app.adapters.http.users.input.user import UserRequest, UserStatusRequest
from app.adapters.http.users.output.user import UserResponse
from app.dependencies.dependencies import user_usecases_dependency
from app.domain.users.command.user_update_status_command import UpdateUserStatusCommand
from app.domain.users.usecases.user_usecases import UserUseCases
from app.dependencies.dependencies import user_token_validation

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    '/users/{user_id}',
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    tags=["Get User by Id"],
)
async def get_user(
    user_id: str,
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
    user_from_token=Depends(user_token_validation),
):
    logger.info("Get user by id called")
    user = user_usecases.find_by_id(user_id)
    return user


@router.get(
    '/users',
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    tags=["Get Users"],
)
async def get_users(
    user_from_token=Depends(user_token_validation),
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    logger.info("Get all users called")
    return user_usecases.list()


@router.post(
    '/users',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Creat an User"],
)
async def create_users(
    user_request: UserRequest,
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    logger.info("Create user called")
    return user_usecases.register(user_request.to_create_user_command())


@router.patch(
    '/users/{user_id}/status',
    response_model=UserResponse,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["update user status"],
)
async def update_status_users(
    user_id: str,
    user_status_request: UserStatusRequest,
    user_from_token=Depends(user_token_validation),
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    logger.info("Update user status called")
    return user_usecases.update_status(
        UpdateUserStatusCommand(user_id=user_id, status=user_status_request.status)
    )
