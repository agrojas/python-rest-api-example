from typing import List
import logging

from app.entities.user import User

logger = logging.getLogger(__name__)


class UsersService:

    def get_users(self) -> List[User]:
        logger.info("Get all users")
        user = User(username="User1", email="email@gmail.com")
        print(user)
        return [user]
