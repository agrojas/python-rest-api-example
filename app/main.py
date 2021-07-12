from app.adapters.http.users import users_controller, users_authentication_controller
from fastapi import FastAPI
import logging


logging.config.fileConfig('app/conf/logging.conf', disable_existing_loggers=False)


app = FastAPI()


logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    logger.info("Startup APP")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutdown APP")


app.include_router(users_controller.router)
app.include_router(users_authentication_controller.router)
