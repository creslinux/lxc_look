import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer

from starlette.config import Config

from platform_controller.platform_controller  import AppController
from platform_usecases.app_usecases import UseCase, PlatformUseCase
from platform_usecases.app_oauth import PlatformSecureCase


config = Config('.env')

app = FastAPI()

# Define the auth scheme and access token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app.mount("/static", StaticFiles(directory="static"), name="static")
AppController(app, PlatformUseCase(), PlatformSecureCase(), config=config)

# def startup(use_case: UseCase = PlatformUseCase():)
    # app = FastAPI()
    # AppController(app, use_case)
    # return app

# if __name__ == "__main__":
#     uvicorn.run(startup(), host="0.0.0.0", port=8090)