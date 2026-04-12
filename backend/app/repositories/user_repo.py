from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User
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
