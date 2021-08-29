from typing import Optional

from pydantic.main import BaseModel


class UserQuery(BaseModel):
    q: Optional[str] = None
    offset: int = 0
    limit: int = 100
