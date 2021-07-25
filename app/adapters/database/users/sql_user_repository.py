from typing import List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.adapters.database.users.model import UserDTO
from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId
from app.domain.users.repository.user_repository import UserRepository


class SQLUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def save(self, user: User):
        user_dto = UserDTO.from_entity(user)
        try:
            self.session.add(user_dto)
        except Exception:
            raise

    def find_by_id(self, user_id: UserId) -> User:
        try:
            user_dto = self.session.query(UserDTO).filter_by(id=user_id.id).one()
        except NoResultFound:
            return None
        except Exception:
            raise
        return user_dto.to_entity()

    def find_by_username(self, username: str) -> User:
        try:
            user_dto = self.session.query(UserDTO).filter_by(username=username).one()
        except NoResultFound:
            return None
        except Exception:
            raise
        return user_dto.to_entity()

    def all(self) -> List[User]:
        return [u.to_entity() for u in self.session.query(UserDTO).all()]

    def total(self) -> int:
        return self.session.query(UserDTO).count()
