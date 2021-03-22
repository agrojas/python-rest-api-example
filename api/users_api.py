import logging

from fastapi import APIRouter, Depends
from typing import List

from api.models.user import UserResponse
from services.users_service import UsersService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/api/users', response_model=List[UserResponse])
async def get_users(service: UsersService = Depends(UsersService)):
    logger.info("Get all users called")
    return service.get_users()
