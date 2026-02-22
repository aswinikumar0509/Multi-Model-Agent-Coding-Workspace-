# app/core/storage.py
from typing import Dict
from .models import Workspace


class InMemoryStorage:
    def __init__(self) -> None:   
        self.workspaces: Dict[str, Workspace] = {}

    def add_workspace(self, ws: Workspace) -> None:
        self.workspaces[ws.id] = ws

    def get_workspace(self, ws_id: str) -> Workspace | None:
        return self.workspaces.get(ws_id)

    def list_workspaces(self) -> list[Workspace]:
        return list(self.workspaces.values())


# Create global instance
storage = InMemoryStorage()
