from sqlalchemy import select, func, distinct, or_
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User
from ..models.project import Project
from ..models.task import Task
from typing import Optional, Sequence
import uuid

async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_by_id(db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def create(db: AsyncSession, name: str, email: str, hashed_password: str) -> User:
    user = User(name=name, email=email, password=hashed_password)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user

async def list_users(db: AsyncSession) -> Sequence[User]:
    result = await db.execute(select(User).order_by(User.name.asc(), User.email.asc()))
    return result.scalars().all()

async def get_user_stats(db: AsyncSession, user_id: uuid.UUID) -> dict:
    owned_projects_result = await db.execute(select(func.count(Project.id)).where(Project.owner_id == user_id))
    projects_owned = owned_projects_result.scalar_one()

    open_tasks_result = await db.execute(
        select(func.count(Task.id)).where(
            Task.assignee_id == user_id,
            Task.status.in_(['todo', 'in_progress'])
        )
    )
    open_tasks = open_tasks_result.scalar_one()

    completed_tasks_result = await db.execute(
        select(func.count(Task.id)).where(
            Task.assignee_id == user_id,
            Task.status == 'done'
        )
    )
    completed_tasks = completed_tasks_result.scalar_one()

    total_projects_result = await db.execute(
        select(func.count(distinct(Project.id)))
        .outerjoin(Task, Task.project_id == Project.id)
        .where(
            or_(Project.owner_id == user_id, Task.assignee_id == user_id)
        )
    )
    total_projects = total_projects_result.scalar_one()

    return {
        "total_projects": total_projects,
        "projects_owned": projects_owned,
        "open_tasks": open_tasks,
        "completed_tasks": completed_tasks
    }
