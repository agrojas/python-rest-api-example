from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.database.users.model import UserDTO
from app.conf.config import Settings


# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
def get_database_url(database_url: str) -> str:
    uri = database_url
    if uri.startswith("postgres://"):
        return uri.replace("postgres://", "postgresql://", 1)
    return uri


def get_session_factory(settings: Settings):
    engine = create_engine(get_database_url(settings.database_url))
    UserDTO.__table__.create(bind=engine, checkfirst=True)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)
