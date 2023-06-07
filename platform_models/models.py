from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from pathlib import Path
from ipaddress import IPv4Address, IPv4Network


BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "../templates"))

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