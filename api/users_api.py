from fastapi import APIRouter, Depends
from typing import List

from api.models.user import UserResponse
from services.users_service import UsersService

router = APIRouter()


@router.get('/api/users', response_model=List[UserResponse])
async def get_users(service: UsersService = Depends(UsersService)):
    return service.get_users()
