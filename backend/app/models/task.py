from sqlalchemy import Column, String, Text, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, UUIDMixin, TimestampMixin
import enum


def enum_values(enum_cls: type[enum.Enum]) -> list[str]:
    return [member.value for member in enum_cls]

class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tasks"

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(TaskStatus, values_callable=enum_values, name="taskstatus"),
        default=TaskStatus.TODO,
        nullable=False,
    )
    priority = Column(
        Enum(TaskPriority, values_callable=enum_values, name="taskpriority"),
        default=TaskPriority.MEDIUM,
        nullable=False,
    )
    
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    due_date = Column(Date, nullable=True)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")
