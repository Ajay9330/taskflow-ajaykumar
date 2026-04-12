from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.task import Task, TaskStatus
from typing import List, Optional
import uuid

async def get_project_tasks(
    db: AsyncSession, 
    project_id: uuid.UUID, 
    status: Optional[TaskStatus] = None, 
    assignee_id: Optional[uuid.UUID] = None,
    limit: int = 20,
    offset: int = 0
) -> List[Task]:
    stmt = select(Task).where(Task.project_id == project_id)
    if status:
        stmt = stmt.where(Task.status == status)
    if assignee_id:
        stmt = stmt.where(Task.assignee_id == assignee_id)
    
    stmt = stmt.limit(limit).offset(offset)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_by_id(db: AsyncSession, task_id: uuid.UUID) -> Optional[Task]:
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()

async def create(db: AsyncSession, project_id: uuid.UUID, **fields) -> Task:
    task = Task(project_id=project_id, **fields)
    db.add(task)
    await db.flush()
    await db.refresh(task)
    return task

async def update(db: AsyncSession, task: Task, data: dict) -> Task:
    for key, value in data.items():
        setattr(task, key, value)
    await db.flush()
    await db.refresh(task)
    return task

async def delete(db: AsyncSession, task: Task) -> None:
    await db.delete(task)
    await db.flush()
