from datetime import timedelta, datetime
from jose import jwt
from app.conf.config import Settings


class JwtUserSigner:
    def __init__(self, settings: Settings):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes

    def create_access_token(self, username: str):
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode = {"sub": username, "exp": expire}
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
