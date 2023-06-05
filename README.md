# LXC, cgroup VMs 
Repo to explore LXC CRUD

The purpose here is, for me, to familiarize with LXC 
namespaces/containers against current KVM knowledge

## How to Run
To run development in mode, `python -m uvicorn de:app --reload`

## What am i looking at
An insecure wrap of the lxc python module with FastAPI

## What am i NOT looking at
Anything production, 
 - there is no AuthZ/N here
 - there is no monitoring here
 - there is no backup/snapshot here

## Install 
Requires local install of lxc and lxc-dev
Install Python deps into venv `pip3 install -r requiremens.txt`

## Nothing of production value here... just playing.
all you bases are belong to us!

