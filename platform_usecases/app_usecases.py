from abc import abstractmethod

import lxc
from fastapi import FastAPI, Body, BackgroundTasks, HTTPException, Request
from platform_models.models import Container


from os import sys
from pathlib import Path


class UseCase:

    @abstractmethod
    def container_exists(self):
        pass

    @abstractmethod
    def list_containers(self):
        pass

    @abstractmethod
    def get_container(self):
        pass

    @abstractmethod
    def give_container_info(self):
        pass

    @abstractmethod
    def raise_409_existbool(self):
        pass

    @abstractmethod
    def build_container(self):
        pass

    @abstractmethod
    def start_container(self):
        pass

    @abstractmethod
    def stop_container(self):
        pass

    @abstractmethod
    def destroy_container(self):
        pass

    @abstractmethod
    def list_files(self):
        pass


class PlatformUseCase(UseCase):
    def container_exists(self, container_name: str):
        if container_name in lxc.list_containers():
            return True
        return False

    def list_containers(self):
        _ret: dict = {}

        for i in lxc.list_containers():
            _c = lxc.Container(name=i)
            _ret = self.give_container_info(
                container=_c, name=i, _ret=_ret, short=True
            )
        return _ret

    def get_container(self, container_name: str):
            # give all about a container
            _ret:dict  = {}
            if not lxc.Container(name=container_name):
                self.raise_409_existbool(
                    container_name=container_name, exists=False
                )
            _c = lxc.Container(name=container_name)
            _ret = self.give_container_info(
                container=_c, name=container_name, _ret={}, short=False
            )
            return _ret

    def give_container_info(
        self, container: object, name: str, _ret: dict, short: bool = True
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

    def raise_409_existbool(self, container_name: str, exists: bool = False):
        _s = "does not" if exists is False else "already"
        raise HTTPException(
            status_code=409,
            detail=f"Container with name {container_name} {_s} exists",
        )

    def build_container(self, ctr: Container):
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

    def start_container(self, container_name: str):
        if not container_name in lxc.list_containers():
            self.raise_409_existbool(container_name=container_name, exists=False)

        if lxc.Container(name=container_name).state == "RUNNING":
            raise HTTPException(
                status_code=409, detail=f"Container already in the Running state"
            )

        if not lxc.Container(name=container_name).start():
            raise HTTPException(status_code=409, detail=f"Container failed to start")

    def stop_container(self, container_name: str):
        if not container_name in lxc.list_containers():
            self.raise_409_existbool(container_name=container_name, exists=False)

        if lxc.Container(name=container_name).state == "STOPPED":
            raise HTTPException(
                status_code=409, detail=f"Container is already in the Stopped state"
            )

        if not lxc.Container(name=container_name).stop():
            raise HTTPException(status_code=409, detail=f"Container failed to stop")

    def destroy_container(self, container_name: str):
        if not container_name in lxc.list_containers():
                self.raise_409_existbool(container_name=container_name, exists=False)
        try:
            if lxc.Container(name=container_name).state == "RUNNING":
                lxc.Container(name=container_name).stop()
        finally:
            if not lxc.Container(name=container_name).destroy():
                raise HTTPException(status_code=409, detail=f"Container failed to destroy")
            
    def list_files(self, request: Request):
        # SRC code explorer for interview
        files = [f.name for f in Path("static").iterdir() if f.is_file()]
        file_paths = sorted([f"/static/{f}" for f in files])
        return file_paths


