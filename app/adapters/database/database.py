from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.database.users.model import UserDTO
from app.conf.config import DATABASE_URL, is_local_env


def get_args():
    return DATABASE_URL + "?check_same_thread=true" if is_local_env() else DATABASE_URL


def get_session_factory():
    engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
    UserDTO.__table__.create(bind=engine, checkfirst=True)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False,)
