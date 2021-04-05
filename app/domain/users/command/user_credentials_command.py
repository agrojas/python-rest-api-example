from pydantic.main import BaseModel


class UserCredentialsCommand(BaseModel):
    username: str
    password: str
