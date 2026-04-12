from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from ..repositories import user_repo
from ..services import auth_service
from ..errors.exceptions import UnauthorizedError, ValidationError

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await user_repo.get_by_email(db, data.email)
    if existing_user:
        raise ValidationError("User already exists", fields={"email": "Email is already registered"})
    
    hashed_password = auth_service.hash_password(data.password)
    user = await user_repo.create(db, data.name, data.email, hashed_password)
    await db.commit()
    
    token = auth_service.create_access_token({
        "sub": user.email,
        "user_id": str(user.id),
        "email": user.email
    })
    return {
        "token": token,
        "user": user
    }

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await user_repo.get_by_email(db, data.email)
    if not user or not auth_service.verify_password(data.password, user.password):
        raise UnauthorizedError("Invalid email or password")
    
    token = auth_service.create_access_token({
        "sub": user.email,
        "user_id": str(user.id),
        "email": user.email
    })
    return {
        "token": token,
        "user": user
    }
