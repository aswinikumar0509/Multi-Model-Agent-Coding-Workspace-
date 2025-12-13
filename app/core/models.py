from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel

LanguageId = Literal["plaintext", "python", "javascript", "cpp"]

class FileNode(BaseModel):
    name:str
    path:str
    Language:LanguageId
    content:str=""

class FolderNode(BaseModel):
    id:str
    name:str
    root_path:str
    root:FolderNode

class WorkspaceCreate(BaseModel):
    name:str
    root_path:str

class WorkspaceSummary(BaseModel):
    id:str
    name:str
    root_path:str

class FileCreate(BaseModel):
    rel_path:str
    is_folder:bool = False
    initial_content:str

class FileUpdate(BaseModel):
    content:str

class FileInfo(BaseModel):
    rel_path:str
    is_folder:bool
    language:LanguageId|None=None
    content:Optional[str]=None
    