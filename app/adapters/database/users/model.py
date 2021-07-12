import time
from typing import Union

from sqlalchemy import Column, String, Boolean, BigInteger, types
from sqlalchemy.orm import declarative_base

from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId

Base = declarative_base()


class UserDTO(Base):
    __tablename__ = "users"

    id: Union[str, Column] = Column(String, primary_key=True, index=True)
    email: Union[str, Column] = Column(String, unique=True, index=True)
    username: Union[str, Column] = Column(String, unique=True, index=True)
    full_name: Union[str, Column] = Column(String)
    hashed_password: Union[str, Column] = Column(String)
    is_active: Union[bool, Column] = Column(Boolean, default=True)
    created_at: Union[int, Column] = Column(BigInteger, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(BigInteger, index=True, nullable=False)

    @staticmethod
    def from_entity(user: User) -> "UserDTO":
        return UserDTO(
            id=user.id.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=user.password,
            is_active=user.is_active,
            created_at=time.time(),
            updated_at=time.time(),
        )

    def to_entity(self) -> User:
        return User(
            id=UserId(self.id),
            email=self.email,
            username=self.username,
            full_name=self.full_name,
            password=self.hashed_password,
            is_active=self.is_active,
        )
