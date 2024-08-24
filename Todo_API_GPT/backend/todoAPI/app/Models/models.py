# from typing import Optional
# from sqlmodel import SQLModel, Field

# class TodoBase(SQLModel):
#     content: str

# class TodoCreate(TodoBase):
#     pass

# class TodoUpdate(TodoBase):
#     pass

# class Todo(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     content: str = Field(index=True)
from typing import Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field

# Define an enumeration for priority levels
class PriorityLevel(int, Enum):
    HIGH = 1
    MEDIUM_HIGH = 2
    MEDIUM = 3
    MEDIUM_LOW = 4
    LOW = 5

class TodoBase(SQLModel):
    content: str  # The content or description of the task
    status: Optional[str] = Field(default="pending", index=True)  # Status of the task (e.g., pending, completed)
    priority: Optional[PriorityLevel] = Field(default=PriorityLevel.MEDIUM, index=True)  # Priority level using the enum
    due_date: Optional[datetime] = None  # Optional due date for the task

class TodoCreate(TodoBase):
    pass  # Fields required when creating a new task

class TodoUpdate(TodoBase):
    content: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[PriorityLevel] = None
    due_date: Optional[datetime] = None

class Todo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Unique identifier for each task
    content: str = Field(index=True)  # The content or description of the task
    status: Optional[str] = Field(default="pending", index=True)  # Status of the task (e.g., pending, completed)
    priority: Optional[PriorityLevel] = Field(default=PriorityLevel.MEDIUM, index=True)  # Priority level using the enum
    due_date: Optional[datetime] = None  # Optional due date for the task
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Automatically set to current time when created
    updated_at: Optional[datetime] = None  # Updated whenever the task is modified
