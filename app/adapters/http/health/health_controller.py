from fastapi import APIRouter, status, Depends

from app.adapters.http.health.output.health_status_response import HealthStatusResponse
from app.conf.config import Settings
from app.dependencies.dependencies import get_settings

router = APIRouter(tags=["health"])


@router.get(
    '/health',
    response_model=HealthStatusResponse,
    status_code=status.HTTP_200_OK,
)
async def health(settings: Settings = Depends(get_settings)):
    return HealthStatusResponse(status="UP", version=settings.version)
