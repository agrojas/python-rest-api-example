from pydantic import BaseModel

from app.adapters.http.users.output.user import UserId


class UpdateUserStatusCommand(BaseModel):
    user_id: UserId
    status: bool
