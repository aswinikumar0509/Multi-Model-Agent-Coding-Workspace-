from fastapi import APIRouter, HTTPException
from core.models import WorkspaceCreate,WorkspaceSummary
from core.services import create_workspace, list_workspaces, get_workspace

router = APIRouter(prefix="/workspaces" , tags=["workspaces"])

@router.post("/",response_model=WorkspaceSummary)
def create_ws(body:WorkspaceCreate):
    ws = create_workspace(body)
    return WorkspaceSummary(id=ws.id,name=ws.name,root_path=ws.root_path)

@router.get("/",response_model=list[WorkspaceSummary])
def list_ws():
    return [
        WorkspaceSummary(id=ws.id,name=ws.name,root_path=ws.root_path)
        for ws in list_workspaces()
    ]

@router.get("/{ws_id}")
def get_ws_detail(ws_id:str):
    try:
        ws = get_workspace(ws_id=ws_id)
    except ValueError:
        raise HTTPException(status_code=404,detail="Workspace not found")
    return ws

