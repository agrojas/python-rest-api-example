from app.adapters.http.users import users_controller, users_authentication_controller
from fastapi import FastAPI
import logging
import uvicorn


logging.config.fileConfig('app/conf/logging.conf', disable_existing_loggers=False)


api = FastAPI()


logger = logging.getLogger(__name__)


@api.on_event("startup")
async def startup():
    logger.info("Startup APP")


@api.on_event("shutdown")
async def shutdown():
    logger.info("Shutdown APP")


api.include_router(users_controller.router)
api.include_router(users_authentication_controller.router)


if __name__ == '__main__':
    uvicorn.run(api)
