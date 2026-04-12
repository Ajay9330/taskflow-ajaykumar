from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    name: str
    email: EmailStr

class RegisterRequest(UserBase):
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: UUID

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    token: str
    user: UserResponse


class UserListResponse(BaseModel):
    users: list[UserResponse]
