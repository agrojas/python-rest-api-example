from typing import List

from entities.user import User


class UsersService:

    def get_users(self) -> List[User]:
        user = User(username="User1", email="email@gmail.com")
        print(user)
        return [user]
