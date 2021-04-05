from fastapi import HTTPException, status
from jose import jwt, JWTError

# TODO: Use env vars

# to get a string like this run:
# openssl rand -hex 32
from app.domain.users.usecases.user_usecases import UserUseCases

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


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
