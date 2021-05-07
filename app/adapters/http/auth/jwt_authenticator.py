from fastapi import HTTPException, status
from jose import jwt, JWTError
from app.domain.users.usecases.user_usecases import UserUseCases
from app.conf.config import SECRET_KEY, ALGORITHM


class JwtAuthenticator:
    def __init__(self, user_usecases: UserUseCases):
        self.user_usecases = user_usecases

    def authenticate(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = self.user_usecases.find_by_username(username=username)
        if user is None:
            raise credentials_exception
        return user
