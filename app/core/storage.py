from __future__ import annotations
from typing import Dict
from .models import Workspace

class InMemoryStorage:

    def __init__(self)->None:
        self.workspaces:Dict[str:Workspace]={}

    def __init__(self,ws:Workspace)->None:
        self.workspaces[ws.id]=ws

    def get_workspace(self,ws_id:str)->Workspace|None:
        return self.workspaces.get(ws_id)
    
    def list_workspaces(self)->list[Workspace]:
        return list(self.workspaces.values())
    

storage = InMemoryStorage()
