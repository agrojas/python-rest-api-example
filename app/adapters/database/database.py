from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.database.users.model import UserDTO
from app.conf.config import Settings


def get_session_factory(settings: Settings):
    engine = create_engine(
        settings.database_url, connect_args={'check_same_thread': False}
    )
    UserDTO.__table__.create(bind=engine, checkfirst=True)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)
