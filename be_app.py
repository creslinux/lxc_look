import uvicorn
from fastapi import FastAPI

from platform_controller.platform_contoller  import AppController
from platform_usecases.app_usecases import UseCase, PlatformUseCase


def startup(use_case: UseCase = PlatformUseCase()):
    app = FastAPI()
    AppController(app, use_case)
    return app


app = FastAPI()
AppController(app, PlatformUseCase())

def startup(use_case: UseCase = PlatformUseCase()):
    app = FastAPI()
    AppController(app, use_case)
    return app

# if __name__ == "__main__":
#     uvicorn.run(startup(), host="0.0.0.0", port=8090)