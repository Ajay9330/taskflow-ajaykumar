from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date
from ..models.task import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: Optional[UUID] = None
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[UUID] = None
    due_date: Optional[date] = None

class TaskResponse(TaskBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
