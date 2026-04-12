from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..dependencies import get_current_user
from ..repositories import user_repo
from ..schemas.auth import UserListResponse
from ..schemas.user import UserStatsResponse
from ..models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=UserListResponse)
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    users = await user_repo.list_users(db)
    return {"users": users}

@router.get("/stats", response_model=UserStatsResponse)
async def get_user_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stats = await user_repo.get_user_stats(db, current_user.id)
    return stats
