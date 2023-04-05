import logging
from typing import List, Optional

from fastapi import Depends, APIRouter, status

from app.adapters.http.users.input.user import UserRequest, UserStatusRequest
from app.adapters.http.users.output.user import UserResponse
from app.dependencies.dependencies import user_usecases_dependency
from app.domain.users.command.user_update_status_command import UpdateUserStatusCommand
from app.domain.users.usecases.user_usecases import UserUseCases
from app.dependencies.dependencies import user_token_validation
from app.domain.users.query.user_query import UserQuery

router = APIRouter(tags=["users"])
logger = logging.getLogger(__name__)


async def user_query(
    q: Optional[str] = None, offset: int = 0, limit: int = 100
) -> UserQuery:
    return UserQuery(q=q, offset=offset, limit=limit)


@router.get(
    '/users',
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    user_from_token=Depends(user_token_validation),
    user_query: Optional[UserQuery] = Depends(user_query),
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    logger.info("Get all users called")
    return user_usecases.list(user_query)


@router.post(
    '/users',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_users(
    user_request: UserRequest,
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    logger.info("Create user called")
    return user_usecases.register(user_request.to_create_user_command())


@router.get(
    '/users/{user_id}',
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: str,
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
    user_from_token=Depends(user_token_validation),
):
    logger.info("Get user by id called")
    user = user_usecases.find_by_id(user_id)
    return user


@router.patch(
    '/users/{user_id}/status',
    response_model=UserResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_users_status(
    user_id: str,
    user_status_request: UserStatusRequest,
    user_from_token=Depends(user_token_validation),
    user_usecases: UserUseCases = Depends(user_usecases_dependency),
):
    logger.info("Update user status called")
    return user_usecases.update_status(
        UpdateUserStatusCommand(user_id=user_id, status=user_status_request.status)
    )
