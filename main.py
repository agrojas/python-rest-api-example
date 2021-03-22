import uvicorn
from fastapi import FastAPI

from api import users_api

api = FastAPI()


def configure():
    api.include_router(users_api.router)

configure()
if __name__ == '__main__':
    uvicorn.run(api)
