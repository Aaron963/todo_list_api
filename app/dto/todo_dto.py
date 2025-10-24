from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TodoListCreateDTO(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class TodoListUpdateDTO(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class TodoItemCreateDTO(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    due_date: Optional[datetime] = None
    status: Optional[str] = Field(None)
    priority: Optional[str] = Field(None)
    tags: Optional[List[str]] = Field(default_factory=list)

class TodoItemUpdateDTO(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    due_date: Optional[datetime] = None
    status: Optional[str] = Field(None)
    priority: Optional[str] = Field(None)
    tags: Optional[List[str]] = None
    media_url: Optional[str] = None