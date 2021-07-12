from sqlalchemy.orm import Session

from app.domain.users.repository.unit_of_work import AbstractUserUnitOfWork
from app.domain.users.repository.user_repository import UserRepository


class UserUnitOfWork(AbstractUserUnitOfWork):
    def __init__(self, repository: UserRepository, session: Session):
        self.session = session
        self.repository = repository

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
