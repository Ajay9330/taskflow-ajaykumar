from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from .task import TaskResponse

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ProjectDetail(ProjectResponse):
    tasks: List[TaskResponse] = []

class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
