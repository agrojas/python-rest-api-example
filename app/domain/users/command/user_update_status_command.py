from pydantic import BaseModel


class UpdateUserStatusCommand(BaseModel):
    user_id: str
    status: str
