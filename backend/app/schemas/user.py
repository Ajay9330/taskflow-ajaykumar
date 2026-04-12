from pydantic import BaseModel
from typing import Optional

class UserStatsResponse(BaseModel):
    total_projects: int
    projects_owned: int
    open_tasks: int
    completed_tasks: int
