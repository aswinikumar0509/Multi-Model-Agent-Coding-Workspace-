from __future__ import annotations
import os
import uuid
from typing import Union
from .models import Workspace, FolderNode, FileNode
from .models import WorkspaceCreate, FileCreate, FileUpdate
from .language import detect_language
from .storage import storage


def _build_tree(path:str)-> FolderNode:
    entries = os.scandir(path)
    children = list[Union[FolderNode,FileNode]] = []

    for entry in entries:
        full_path = os.path.join(path,entry.name)
        if entry.is_dir():
            children.append(_build_tree(full_path))
        else:
            lang = detect_language(entry.name)
            children.append(FileNode(
                name=entry.name,
                path=full_path,
                language=lang,
                content=""
            ))
    return FolderNode(
        name=os.path.basename(path),
        path=path,
        children=children
    )

def create_workspace(data:WorkspaceCreate)->Workspace:
    ws_id = str(uuid.uuid4())

    os.makedirs(data.root_path,exist_ok=True)
    root = _build_tree(data.root_path)
    ws = Workspace(
        id=ws_id,
        name = data.name,
        root_path = data.root_path,
        root=root,
    )
    storage.add_workspace(ws)
    return ws

def list_workspace(ws_id:str)-> list[Workspace]:
    return storage.list_workspaces

def get_workspace(ws_id:str)->list[Workspace]:
    ws = storage.get_workspace(ws_id=ws_id)
    if not ws:
        raise ValueError("Work space not found")
    return ws

def create_file_or_folder(ws_id:str,file_data:FileCreate):
    ws = get_workspace(ws_id=ws_id)
    abs_path = os.path.join(ws.root_path,file_data.rel_path)

    if file_data.is_folder:
        os.makedirs(abs_path,exist_ok=True)

    else:
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path,"w",encoding="utf-8") as f:
            f.write(file_data.initial_content or "")

    ws.root = _build_tree(ws.root_path)
    storage.add_workspace(ws)
    return ws


def read_file(ws_id:str , rel_path:str)->FileNode:
    ws = get_workspace(ws_id=ws_id)
    abs_path = os.path.join(ws.root_path,rel_path)

    if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
        raise FileNotFoundError("File not found")
    
    with open(abs_path, "r", encoding="utf-8") as f:
        content = f.read()

    lang = detect_language(os.path.basename(abs_path))

    return FileNode(
        name = os.path.basename(abs_path),
        path = abs_path,
        language=lang,
        content=content,
    )

def update_file(ws_id:str,rel_path:str,data:FileUpdate)->FileNode:
    ws = get_workspace(ws_id=ws_id)
    abs_path = os.path.join(ws.root_path,rel_path)

    if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
        raise FileNotFoundError("File not found")
    
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(data.content)

    lang = detect_language(os.path.basename(abs_path))

    return FileNode(
        name = os.path.basename(abs_path),
        path = abs_path,
        language=lang,
        content=data.content,
    )
