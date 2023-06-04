from typing import Annotated, Union
from fastapi import FastAPI, Body, BackgroundTasks, HTTPException
from pydantic import BaseModel
from ipaddress import IPv4Address, IPv4Network

import lxc
import sys

# Very first look at cgroup / lxc ns container / automation
# pydantic models for typing/structure
# swagger for fe / testing / faster dev
# super skinny stack, ubuntu/apt only

app = FastAPI()

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


# hack - this is psuedo persist, that dies on stop
containers: dict[str, Container] = {}

# route helper methods


def build_container(ctr: Container):
    # Create LXC container, -- TODO, Background this task
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


# routes
# # todo - wrap under OpenID AuthN GW,
# # and filter with decorator to condider mutli-tennancy/object owners AuthZ

@app.get("/")
async def list_containers():
    _ret: dict = {}

    for i in lxc.list_containers():
        _c = lxc.Container(name=i)

        _ret[i] = {}
        _ret[i]["name"] = i
        _ret[i]["interfaces"] = _c.get_interfaces()
        _ret[i]["ips"] = _c.get_ips
        _ret[i]["state"] = _c.state

    return {"message": f"Contianers in namespace discovered", "data": _ret}


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


@app.post("/start/")  # todo
async def destroy_container(container_name: str):
    if not container_name in lxc.list_containers():
        raise_409_existbool(container_name=container_name, exists=False)
    if not lxc.Container(name=container_name).start():
        HTTPException(status_code=409, detail=f"Container failed to start")
    return {"message": f"Starting {container_name}", "data": True}


@app.post("/stop/")  # todo
async def destroy_container(container_name: str):
    if not container_name in lxc.list_containers():
        raise_409_existbool(container_name=container_name, exists=False)
    if not lxc.Container(name=container_name).stop():
        HTTPException(status_code=409, detail=f"Container failed to stop")
    return {"message": f"Stoping {container_name}", "data": True}


@app.post("/destroy/")  # todo
async def destroy_container(container_name: str):
    if not container_name in lxc.list_containers():
        raise_409_existbool(container_name=container_name, exists=False)
    try:
        if lxc.Container(name=container_name).state == "RUNNING":
            lxc.Container(name=container_name).stop()
    finally:
        if not lxc.Container(name=container_name).destroy():
            HTTPException(status_code=409, detail=f"Container failed to destroy")
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
async def clone_container(container_name: str, network: Network):
    if not container_name in lxc.list_containers():
        raise_409_existbool(container_name=container_name, exists=False)
    pass
