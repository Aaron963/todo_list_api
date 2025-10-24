from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
import enum
import uuid

class TodoStatus(str, enum.Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class TodoPriority(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class TodoItem(BaseModel):
    item_id: str = Field(
        default_factory=lambda: f"item_{uuid.uuid4().hex[:8]}",
        description="唯一项ID"
    )
    list_id: str = Field(..., description="所属列表ID")
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    due_date: Optional[datetime] = None
    status: TodoStatus = Field(default=TodoStatus.NOT_STARTED)
    priority: TodoPriority = Field(default=TodoPriority.MEDIUM)
    tags: List[str] = Field(default_factory=list)
    media_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Item title cannot be empty")
        return v.strip()

    @validator("tags")
    def tags_uniq(cls, v):
        return list(set(v))  # 去重

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.isoformat()}