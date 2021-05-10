from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.database.users.model import UserDTO
from app.conf.config import DATABASE_URL, is_local_env


def get_args():
    return DATABASE_URL + "?check_same_thread=true" if is_local_env() else DATABASE_URL


engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
UserDTO.__table__.create(bind=engine, checkfirst=True)

DEFAULT_SESSION_FACTORY = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
