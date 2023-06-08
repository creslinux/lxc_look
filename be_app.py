import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from platform_controller.platform_controller  import AppController
from platform_usecases.app_usecases import UseCase, PlatformUseCase


def startup(use_case: UseCase = PlatformUseCase()):
    app = FastAPI()
    AppController(app, use_case)
    return app


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
AppController(app, PlatformUseCase())

def startup(use_case: UseCase = PlatformUseCase()):
    app = FastAPI()
    AppController(app, use_case)
    return app

# if __name__ == "__main__":
#     uvicorn.run(startup(), host="0.0.0.0", port=8090)