class UsersNotFoundError(Exception):
    def __init__(self, user_id: str):
        self.message = f'User {user_id} not found'

    def __str__(self):
        return self.message


class UserAlreadyExistException(Exception):
    message = "This User already exists"

    def __str__(self):
        return UserAlreadyExistException.message


class UserAlreadyHadStatusError(Exception):
    message = "This User already had this status."

    def __str__(self):
        return UserAlreadyHadStatusError.message


class UsersBlockedException(Exception):
    message = "This User is blocked."

    def __str__(self):
        return UsersBlockedException.message
