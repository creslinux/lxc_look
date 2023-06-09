import lxc

from typing import Annotated
from fastapi import FastAPI, Body, BackgroundTasks, Request
from fastapi.responses import HTMLResponse

from platform_usecases.app_usecases import UseCase
from platform_models.models import (
    TEMPLATES,
    Container,
    ToInstall,
    Network,
    containers,
)

from starlette.routing import Mount, Route


class AppController:
    def __init__(self, app: FastAPI, use_case: UseCase):
        # Return list of lxc contianers, and their state
        @app.get("/list_containers/")
        async def list_containers():
            _ret = use_case.list_containers()
            return {f"message": "Returning all containers on host", "data": _ret}

        # Query more detail on a named lxc instance
        @app.get("/get-container/{container_name}/")
        async def get_container(container_name: str):
            _ret = use_case.get_container(container_name=container_name)
            return {f"message": " Success get {container_name}", "data": _ret}

        @app.post("/create-container/")
        async def create_container(
            container: Annotated[
                Container,
                Body(
                    examples={
                        "normal": {
                            "summary": "Example of a normal container",
                            "description": "A **normal** container payload correctly.",
                            "value": {
                                "name": "Foo",
                                "dist": "ubuntu",
                                "release": "lunar",
                                "arch": "amd64",
                            },
                        },
                    },
                ),
            ],
            background_tasks: BackgroundTasks,
        ):
            if container.name in containers or use_case.container_exists(
                container_name=container.name
            ):
                use_case.raise_409_existbool(container_name=container.name, exists=True)
            # take an optimistic record, prevent conflicting builds
            # build as a background task
            containers.update({container.name: container})

            # Enum obj to str
            container.dist = container.dist.name
            container.release = container.release.name
            container.arch = container.arch.name

            background_tasks.add_task(use_case.build_container, ctr=container)
            return {"message": "Sent for build", "container": container}

        @app.post("/start/")
        async def start_container(container_name: str):
            use_case.start_container(container_name=container_name)
            return {"message": f"Starting {container_name}", "data": True}

        @app.post("/stop/")
        async def stop_container(container_name: str):
            use_case.stop_container(container_name=container_name)
            return {"message": f"Stopping {container_name}", "data": True}

        @app.post("/destroy/")
        async def destroy_container(container_name: str):
            use_case.destroy_container(container_name=container_name)
            return {"message": f"Destroyed {container_name}", "data": True}

        # Templated HTML Pages
        @app.get("/", response_class=HTMLResponse)  # template landing page
        async def html_frontpage(request: Request):
            _ret = use_case.list_containers()

            return TEMPLATES.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "data": _ret,
                },
            )

        @app.get("/src/", response_class=HTMLResponse)
        async def list_files(request: Request):
            files_paths = use_case.list_files(request=request)

            return TEMPLATES.TemplateResponse(
                "list_files.html", {"request": request, "files": files_paths}
            )

        # TODO - skeletons to complete
        @app.post("/clone/")  # todo
        async def clone_container(container_name: str, target: Container):
            if not container_name in lxc.list_containers():
                use_case.raise_409_existbool(
                    container_name=container_name, exists=False
                )
            pass

        @app.post("/install-apps/")  # todo
        async def install_apps(container_name: str, toinstall: ToInstall):
            if not container_name in lxc.list_containers():
                use_case.raise_409_existbool(
                    container_name=container_name, exists=False
                )
            pass

        @app.post("/addnetwork/")  # todo
        async def add_network(container_name: str, network: Network):
            if not container_name in lxc.list_containers():
                use_case.raise_409_existbool(
                    container_name=container_name, exists=False
                )
            pass
