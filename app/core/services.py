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