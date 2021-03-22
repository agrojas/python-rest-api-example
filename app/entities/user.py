from pydantic import BaseModel, EmailStr
import uuid
import random
import string


class User(BaseModel):
    username: str
    email: EmailStr
    id = uuid.uuid4()
    secret = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
