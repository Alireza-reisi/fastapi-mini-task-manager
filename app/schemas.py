from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    is_completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    is_completed: bool | None = None


class TaskOut(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TaskQueryParams(BaseModel):
    q: Optional[str] = Field(default=None, min_length=1, description="Search in title/description")
    is_completed: Optional[bool] = Field(default=None, description="Filter by completion status")