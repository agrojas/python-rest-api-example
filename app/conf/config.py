import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'locals')
TITLE = os.getenv('TITLE', 'Default Title')
DESCRIPTION = os.getenv('DESCRIPTION', 'Default Description')
VERSION = os.getenv('VERSION', '1.0')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 1))
DATABASE_URL = os.getenv('DATABASE_URL')


def is_local_env():
    return ENVIRONMENT == "local"
