from fastapi import APIRouter, Depends, Request, status
import asyncio
from fastapi.responses import StreamingResponse
import json
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from ..database import get_db
from ..schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectDetail, ProjectListResponse
from ..services import project_service
from ..dependencies import get_current_user, get_current_user_from_stream
from ..models.user import User
from ..core.events import manager

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("", response_model=ProjectListResponse)
async def list_projects(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    projects = await project_service.get_projects(db, current_user, limit, offset)
    return {"projects": projects}

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return await project_service.create_project(db, current_user, data)

@router.get("/{id}", response_model=ProjectDetail)
async def get_project(
    id: UUID, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return await project_service.get_project_detail(db, id, current_user)

@router.patch("/{id}", response_model=ProjectResponse)
async def update_project(
    id: UUID, 
    data: ProjectUpdate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return await project_service.update_project(db, id, current_user, data)

@router.get("/{id}/stats")
async def get_project_stats(
    id: UUID, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return await project_service.get_project_stats(db, id, current_user)



@router.get("/{id}/events")
async def project_events(
    id: UUID, 
    request: Request,
    current_user: User = Depends(get_current_user_from_stream),
    db: AsyncSession = Depends(get_db),
):
    await project_service.get_project_detail(db, id, current_user)
    
    async def event_generator():
        queue = await manager.subscribe(id)
        try:
            while not await request.is_disconnected():
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=20.0)
                    yield f"data: {json.dumps(event)}\n\n"
                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"
        finally:
            await manager.unsubscribe(id, queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    id: UUID, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    await project_service.delete_project(db, id, current_user)
    return None
