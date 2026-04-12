import sqlalchemy as sa
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ..models.project import Project
from ..models.task import Task
from typing import List, Optional
import uuid

async def get_user_projects(db: AsyncSession, user_id: uuid.UUID, limit: int = 10, offset: int = 0) -> List[Project]:
    # Projects owned by user OR projects where user has assigned tasks
    stmt = select(Project).outerjoin(Task).where(
        or_(
            Project.owner_id == user_id,
            Task.assignee_id == user_id
        )
    ).distinct().limit(limit).offset(offset)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_by_id(db: AsyncSession, project_id: uuid.UUID) -> Optional[Project]:
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()

async def get_accessible_project(
    db: AsyncSession,
    project_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Optional[Project]:
    stmt = (
        select(Project)
        .outerjoin(Task)
        .where(
            Project.id == project_id,
            or_(
                Project.owner_id == user_id,
                Task.assignee_id == user_id,
            ),
        )
        .distinct()
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_with_tasks(db: AsyncSession, project_id: uuid.UUID) -> Optional[Project]:
    stmt = select(Project).where(Project.id == project_id).options(selectinload(Project.tasks))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create(db: AsyncSession, name: str, description: Optional[str], owner_id: uuid.UUID) -> Project:
    project = Project(name=name, description=description, owner_id=owner_id)
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return project

async def update(db: AsyncSession, project: Project, data: dict) -> Project:
    for key, value in data.items():
        setattr(project, key, value)
    await db.flush()
    await db.refresh(project)
    return project

async def get_project_stats(db: AsyncSession, project_id: uuid.UUID):
    # Counts by status
    status_stmt = select(Task.status, sa.func.count(Task.id)).where(Task.project_id == project_id).group_by(Task.status)
    status_result = await db.execute(status_stmt)
    status_counts = {status.value: count for status, count in status_result.all()}

    # Counts by assignee
    assignee_stmt = select(Task.assignee_id, sa.func.count(Task.id)).where(Task.project_id == project_id).group_by(Task.assignee_id)
    assignee_result = await db.execute(assignee_stmt)
    assignee_counts = {str(assignee_id) if assignee_id else "unassigned": count for assignee_id, count in assignee_result.all()}

    return {
        "by_status": status_counts,
        "by_assignee": assignee_counts
    }

async def delete(db: AsyncSession, project: Project) -> None:
    await db.delete(project)
    await db.flush()
