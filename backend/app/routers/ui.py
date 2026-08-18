"""Static dashboard UI (spec 19-21). Serves index.html and mounts /static."""

from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter(tags=["ui"])

_STATIC = Path(__file__).resolve().parent.parent / "static"


@router.get("/")
def index():
    return FileResponse(_STATIC / "index.html")


@router.get("/favicon.ico")
def favicon():
    return FileResponse(_STATIC / "favicon.ico")
