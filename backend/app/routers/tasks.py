from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from ..database import get_db
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from ..services import task_service
from ..dependencies import get_current_user
from ..models.user import User
from ..models.task import TaskStatus

router = APIRouter(tags=["tasks"])

@router.get("/projects/{project_id}/tasks", response_model=TaskListResponse)
async def list_tasks(
    project_id: UUID,
    status: Optional[TaskStatus] = None,
    assignee: Optional[UUID] = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    tasks = await task_service.list_tasks(db, project_id, current_user, status, assignee, limit, offset)
    return {"tasks": tasks}

@router.post("/projects/{project_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    project_id: UUID,
    data: TaskCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return await task_service.create_task(db, project_id, current_user, data)

@router.patch("/tasks/{id}", response_model=TaskResponse)
async def update_task(
    id: UUID, 
    data: TaskUpdate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return await task_service.update_task(db, id, current_user, data)

@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: UUID, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    await task_service.delete_task(db, id, current_user)
    return None
