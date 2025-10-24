from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid

class TodoList(BaseModel):
    list_id: str = Field(
        default_factory=lambda: f"list_{uuid.uuid4().hex[:8]}",
        description="唯一列表ID"
    )
    owner_id: str = Field(..., description="所属用户ID")
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("List title cannot be empty")
        return v.strip()

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.isoformat()}