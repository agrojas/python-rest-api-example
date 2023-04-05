from typing import Union

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId
from app.domain.users.model.user_status import UserStatus

Base = declarative_base()


class UserDTO(Base):
    __tablename__ = "users"

    id: Union[str, Column] = Column(String, primary_key=True, index=True)
    email: Union[str, Column] = Column(String, unique=True, index=True)
    username: Union[str, Column] = Column(String, unique=True, index=True)
    full_name: Union[str, Column] = Column(String)
    hashed_password: Union[str, Column] = Column(String)
    status: Union[str, Column] = Column(String, default=True)
    created_at: Union[DateTime, Column] = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Union[DateTime, Column] = Column(
        DateTime(timezone=True), onupdate=func.now()
    )

    @staticmethod
    def from_entity(user: User) -> "UserDTO":
        return UserDTO(
            id=user.id.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=user.password,
            status=user.status,
        )

    def to_entity(self) -> User:
        return User(
            id=UserId(self.id),
            email=self.email,
            username=self.username,
            full_name=self.full_name,
            password=self.hashed_password,
            status=UserStatus(self.status),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
