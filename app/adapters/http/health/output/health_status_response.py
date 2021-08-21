from pydantic.main import BaseModel


class HealthStatusResponse(BaseModel):
    api_version: str
    status: str
