import logging

import uvicorn
from fastapi import FastAPI

from app.adapters.http.users import users_controller, users_authentication_controller

# setup loggers
logging.config.fileConfig('app/conf/logging.conf', disable_existing_loggers=False)

api = FastAPI()

logger = logging.getLogger(__name__)


@api.on_event("startup")
async def startup():
    logger.info("Startup APP")


@api.on_event("shutdown")
async def shutdown():
    logger.info("Shutdown APP")


def configure():
    api.include_router(users_controller.router)
    api.include_router(users_authentication_controller.router)


configure()
if __name__ == '__main__':
    uvicorn.run(api)
