# app/api/files.py
from __future__ import annotations
from fastapi import APIRouter, HTTPException

from core.models import FileCreate, FileUpdate, FileInfo
from core.services import create_file_or_folder, read_file, update_file

router = APIRouter(prefix="/workspaces/{ws_id}/files", tags=["files"])


@router.post("/", response_model=None)
def create_file(ws_id: str, body: FileCreate):
    try:
        create_file_or_folder(ws_id, body)
    except ValueError:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return {"status": "ok"}


@router.get("/", response_model=FileInfo)
def get_file(ws_id: str, rel_path: str):
    try:
        node = read_file(ws_id, rel_path)
    except ValueError:
        raise HTTPException(status_code=404, detail="Workspace not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

    return FileInfo(
        rel_path=rel_path,
        is_folder=False,
        language=node.language,
        content=node.content
    )


@router.put("/", response_model=FileInfo)
def update_file_content(ws_id: str, rel_path: str, body: FileUpdate):
    try:
        node = update_file(ws_id, rel_path, body)
    except ValueError:
        raise HTTPException(status_code=404, detail="Workspace not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

    return FileInfo(
        rel_path=rel_path,
        is_folder=False,
        language=node.language,
        content=node.content
    )
