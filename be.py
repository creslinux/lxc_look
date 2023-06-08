from typing import Annotated, Union
from fastapi import FastAPI, Body, BackgroundTasks, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from ipaddress import IPv4Address, IPv4Network

from pathlib import Path

import lxc
import sys


BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(title="lxc fastapi LXC CRUD")
app.mount("/static", StaticFiles(directory="static"), name="static")

# LXC structures


# Todo: how to set cgroup limits on a container?
class Container(BaseModel):
    name: str
    dist: str = "ubuntu"
    release: str
    arch: str = "amd64"


# Only considering unbuntu apt here..
class ToInstall(BaseModel):
    apps: list


class Network(BaseModel):
    device: str
    network: IPv4Network
    ip_addr: IPv4Address
    default_gw: IPv4Address


# hack - this is psuedo persist, for dev use and single node only
containers: dict[str, Container] = {}


# route helper methods
def build_container(ctr: Container):
    # Create LXC container in backkground
    try:
        _c = lxc.Container(ctr.name)
        _c.create(
            "download",
            lxc.LXC_CREATE_QUIET,
            {"dist": ctr.dist, "release": ctr.release, "arch": "amd64"},
        )
    except Exception as e:  # todo create custom raise for the app
        print("Failed to create the container rootfs", file=sys.stderr)


def raise_409_existbool(container_name: str, exists: bool = False):
    _s = "does not" if exists is False else "already"
    raise HTTPException(
        status_code=409,
        detail=f"Container with name {container_name} {_s} exists",
    )


def give_container_info(
    container: object, name: str, _ret: dict, short: bool = True
) -> dict:
    _ret[name] = {}
    _ret[name]["name"] = name
    _ret[name]["interfaces"] = container.get_interfaces()
    _ret[name]["ips"] = container.get_ips()
    _ret[name]["state"] = container.state
    if short:
        return _ret

    _ret[name]["keys"] = container.get_keys()
    _ret[name]["console_fd"] = container.console_getfd()
    return _ret


# routes
# # todo - nb this is not under OpenID AuthN GW,
# # there are no filters considering mutli-tennancy/object owners AuthZ


@app.get("/list_containers/")
async def list_containers():
    _ret: dict = {}

    for i in lxc.list_containers():
        _c = lxc.Container(name=i)
        _ret = give_container_info(container=_c, name=i, _ret=_ret, short=True)

    return {f"message": "Returning all containers on host", "data": _ret}


@app.get("/get-container/{container_name}/")
async def get_container(container_name: str):
    container_name: str
    # give all about a containe
    if not lxc.Container(name=container_name):
        raise_409_existbool(container_name=container_name, exists=False)
    _c = lxc.Container(name=container_name)
    _ret = give_container_info(container=_c, name=container_name, _ret={}, short=False)

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
    #  we begin, annotated fastapi sigs ^ really big - but nice
    if container.name in containers:
        raise_409_existbool(container_name=container.name, exists=True)
    # take an optimistic record, prevent conflicting builds
    # build as bg task to not timeout, builds can be a minute..
    containers.update({container.name: container})
    background_tasks.add_task(build_container, ctr=container)
    return {"message": "Sent for build", "container": container}


@app.post("/start/") 
async def start_container(container_name: str):
    if not container_name in lxc.list_containers():
        raise_409_existbool(container_name=container_name, exists=False)

    if lxc.Container(name=container_name).state == "RUNNING":
        raise HTTPException(
            status_code=409, detail=f"Container already in the Running state"
        )

    if not lxc.Container(name=container_name).start():
        raise HTTPException(status_code=409, detail=f"Container failed to start")

    return {"message": f"Starting {container_name}", "data": True}


@app.post("/stop/")  
async def stop_container(container_name: str):
    if not container_name in lxc.list_containers():
        raise_409_existbool(container_name=container_name, exists=False)

    if lxc.Container(name=container_name).state == "STOPPED":
        raise HTTPException(
            status_code=409, detail=f"Container is already in the Stopped state"
        )

    if not lxc.Container(name=container_name).stop():
        raise HTTPException(status_code=409, detail=f"Container failed to stop")

    return {"message": f"Stopping {container_name}", "data": True}


@app.post("/destroy/")  
async def destroy_container(container_name: str):
    if not container_name in lxc.list_containers():
        raise_409_existbool(container_name=container_name, exists=False)
    try:
        if lxc.Container(name=container_name).state == "RUNNING":
            lxc.Container(name=container_name).stop()
    finally:
        if not lxc.Container(name=container_name).destroy():
            raise HTTPException(status_code=409, detail=f"Container failed to destroy")
    return {"message": f"Destroyed {container_name}", "data": True}


# TODO - skeletons to complete
@app.post("/clone/")  # todo
async def clone_container(container_name: str, target: Container):
    if not container_name in lxc.list_containers():
        raise_409_existbool(container_name=container_name, exists=False)
    pass


@app.post("/install-apps/")  # todo
async def install_apps(container_name: str, toinstall: ToInstall):
    if not container_name in lxc.list_containers():
        raise_409_existbool(container_name=container_name, exists=False)
    pass


@app.post("/addnetwork/")  # todo
async def add_network(container_name: str, network: Network):
    if not container_name in lxc.list_containers():
        raise_409_existbool(container_name=container_name, exists=False)
    pass


# HTML landing page
@app.get("/", response_class=HTMLResponse)  # template landing page
async def html_frontpage(request: Request):
    _ret: dict = {}

    for i in lxc.list_containers():
        _c = lxc.Container(name=i)
        _ret = give_container_info(container=_c, name=i, _ret=_ret, short=True)

    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "data": _ret,
        },
    )

@app.get("/src/", response_class=HTMLResponse)
async def list_files(request: Request):

    # SRC code explorer for interview
    files = [f.name for f in Path("static").iterdir() if f.is_file()]
    file_paths = sorted([f"/static/{f}" for f in files])

    return TEMPLATES.TemplateResponse(
        "list_files.html", 
        {
            "request": request, 
            "files": file_paths
        }
    )
