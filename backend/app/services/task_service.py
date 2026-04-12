from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories import task_repo, project_repo, user_repo
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ..errors.exceptions import NotFoundError, ForbiddenError, ValidationError
from ..models.user import User
from ..models.task import TaskStatus
from ..core.events import manager
import uuid
from typing import Optional
from .access_service import require_project_access

async def list_tasks(
    db: AsyncSession, 
    project_id: uuid.UUID, 
    current_user: User, 
    status: Optional[TaskStatus] = None, 
    assignee_id: Optional[uuid.UUID] = None,
    limit: int = 20,
    offset: int = 0
):
    await require_project_access(db, project_id, current_user)
    return await task_repo.get_project_tasks(db, project_id, status, assignee_id, limit, offset)

async def create_task(db: AsyncSession, project_id: uuid.UUID, current_user: User, data: TaskCreate):
    await require_project_access(db, project_id, current_user)

    if data.assignee_id:
        assignee = await user_repo.get_by_id(db, data.assignee_id)
        if not assignee:
            raise ValidationError("Assignee not found", fields={"assignee_id": "User does not exist"})

    task_data = data.model_dump()
    new_task = await task_repo.create(db, project_id, **task_data)
    await db.commit()

    await manager.broadcast(project_id, {
        "type": "task_created",
        "task": TaskResponse.model_validate(new_task).model_dump(mode="json")
    })

    return new_task

async def update_task(db: AsyncSession, task_id: uuid.UUID, current_user: User, data: TaskUpdate):
    task = await task_repo.get_by_id(db, task_id)
    if not task:
        raise NotFoundError("Task not found")

    await require_project_access(db, task.project_id, current_user)

    if data.assignee_id:
        assignee = await user_repo.get_by_id(db, data.assignee_id)
        if not assignee:
            raise ValidationError("Assignee not found", fields={"assignee_id": "User does not exist"})

    update_data = data.model_dump(exclude_unset=True)
    updated_task = await task_repo.update(db, task, update_data)
    await db.commit()

    await manager.broadcast(task.project_id, {
        "type": "task_updated",
        "task": TaskResponse.model_validate(updated_task).model_dump(mode="json")
    })

    return updated_task

async def delete_task(db: AsyncSession, task_id: uuid.UUID, current_user: User):
    task = await task_repo.get_by_id(db, task_id)
    if not task:
        raise NotFoundError("Task not found")

    project_id = task.project_id
    project = await require_project_access(db, project_id, current_user)
    if project.owner_id != current_user.id:
        raise ForbiddenError("Only the project owner can delete tasks")

    await task_repo.delete(db, task)
    await db.commit()

    await manager.broadcast(project_id, {
        "type": "task_deleted",
        "task_id": str(task_id)
    })
