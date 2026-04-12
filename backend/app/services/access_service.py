import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from ..errors.exceptions import ForbiddenError, NotFoundError
from ..models.project import Project
from ..models.user import User
from ..repositories import project_repo


async def require_project_access(
    db: AsyncSession,
    project_id: uuid.UUID,
    current_user: User,
) -> Project:
    project = await project_repo.get_accessible_project(db, project_id, current_user.id)
    if not project:
        raise NotFoundError("Project not found")
    return project


async def require_project_owner(
    db: AsyncSession,
    project_id: uuid.UUID,
    current_user: User,
) -> Project:
    project = await require_project_access(db, project_id, current_user)
    if project.owner_id != current_user.id:
        raise ForbiddenError("Only the project owner can perform this action")
    return project
