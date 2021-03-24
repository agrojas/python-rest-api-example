import logging

from fastapi import APIRouter, Depends
from typing import List

from app.adapters.database.users.in_memory_user_repository import InMemoryUserRepository
from app.adapters.http.users.input.user import UserRequest
from app.adapters.http.users.output.user import UserResponse
from app.domain.users.usecases.user_usecases import UserUseCases

router = APIRouter()
logger = logging.getLogger(__name__)

user_repository = InMemoryUserRepository()
user_usecases = UserUseCases(user_repository)


@router.get('/users', response_model=List[UserResponse])
async def get_users():
    logger.info("Get all users called")
    return user_usecases.list()


@router.post('/users', response_model=UserResponse)
async def create_users(user_request: UserRequest):
    logger.info("Get all users called")
    user = user_usecases.register(user_request.to_create_user_command())
    return user
