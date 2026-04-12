from fastapi import Depends, Query, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .services import auth_service
from .repositories import user_repo
from .errors.exceptions import UnauthorizedError
from .models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def resolve_user_from_token(db: AsyncSession, token: str) -> User:
    payload = auth_service.decode_token(token)
    if not payload:
        raise UnauthorizedError("Could not validate credentials")

    email: str | None = payload.get("sub")
    if email is None:
        raise UnauthorizedError("Could not validate credentials")

    user = await user_repo.get_by_email(db, email=email)
    if user is None:
        raise UnauthorizedError("User not found")

    return user

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    return await resolve_user_from_token(db, token)


async def get_current_user_from_stream(
    request: Request,
    token: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    resolved_token = token
    if not resolved_token:
        authorization = request.headers.get("authorization", "")
        if authorization.lower().startswith("bearer "):
            resolved_token = authorization.split(" ", 1)[1].strip()

    if not resolved_token:
        raise UnauthorizedError("Could not validate credentials")

    return await resolve_user_from_token(db, resolved_token)
