from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories import project_repo
from ..schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from ..errors.exceptions import NotFoundError
from ..models.user import User
from ..core.events import manager
import uuid
from .access_service import require_project_access, require_project_owner

async def get_projects(db: AsyncSession, current_user: User, limit: int = 10, offset: int = 0):
    return await project_repo.get_user_projects(db, current_user.id, limit, offset)

async def create_project(db: AsyncSession, current_user: User, data: ProjectCreate):
    project = await project_repo.create(db, data.name, data.description, current_user.id)
    await db.commit()
    return project

async def get_project_detail(db: AsyncSession, project_id: uuid.UUID, current_user: User):
    accessible_project = await require_project_access(db, project_id, current_user)
    project = await project_repo.get_with_tasks(db, accessible_project.id)
    if not project:
        raise NotFoundError("Project not found")
    return project

async def update_project(db: AsyncSession, project_id: uuid.UUID, current_user: User, data: ProjectUpdate):
    project = await require_project_owner(db, project_id, current_user)
    update_data = data.model_dump(exclude_unset=True)
    updated_project = await project_repo.update(db, project, update_data)
    await db.commit()

    await manager.broadcast(project.id, {
        "type": "project_updated",
        "project": ProjectResponse.model_validate(updated_project).model_dump(mode="json")
    })

    return updated_project

async def get_project_stats(db: AsyncSession, project_id: uuid.UUID, current_user: User):
    await require_project_access(db, project_id, current_user)
    return await project_repo.get_project_stats(db, project_id)

async def delete_project(db: AsyncSession, project_id: uuid.UUID, current_user: User):
    project = await require_project_owner(db, project_id, current_user)
    await project_repo.delete(db, project)
    await db.commit()
