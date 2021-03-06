import uvicorn


from app.adapters.http.auth.exceptions.authentication_exception import (
    AuthenticationException,
)
from app.adapters.http.users.exceptions_handler import (
    validation_exception_handler,
    user_already_exist_exception_handler,
    user_already_had_status_exception_handler,
    user_not_found_exception_handler,
    user_blocked_exception_handler,
    wrong_credentials_exception_handler,
)
from app.adapters.http.users import users_controller
from app.adapters.http.auth import authentication_controller
from app.adapters.http.health import health_controller
from fastapi import FastAPI
import logging.config

from app.conf.config import Settings
from app.domain.users.model.user_exceptions import (
    UserAlreadyExistException,
    UserAlreadyHadStatusError,
    UsersNotFoundError,
    InvalidCredentialsError,
    UsersBlockedException,
)

logging.config.fileConfig('app/conf/logging.conf', disable_existing_loggers=False)

settings = Settings()

app = FastAPI(
    version=settings.version, title=settings.title, description=settings.description
)

logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    logger.info("Startup APP")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutdown APP")


app.include_router(users_controller.router, prefix=settings.version_prefix)
app.include_router(authentication_controller.router, prefix=settings.version_prefix)

app.include_router(health_controller.router)

app.add_exception_handler(AuthenticationException, validation_exception_handler)
app.add_exception_handler(
    UserAlreadyExistException, user_already_exist_exception_handler
)
app.add_exception_handler(
    UserAlreadyHadStatusError, user_already_had_status_exception_handler
)
app.add_exception_handler(UsersNotFoundError, user_not_found_exception_handler)
app.add_exception_handler(InvalidCredentialsError, wrong_credentials_exception_handler)

app.add_exception_handler(UsersBlockedException, user_blocked_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)
