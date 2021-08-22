from pydantic.main import BaseModel


class HealthStatusResponse(BaseModel):
    version: str
    status: str
