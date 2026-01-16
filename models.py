from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100) # # Защита от слишком больших данных
    text: Optional[str] = Field(None, max_length=500) # Защита от слишком больших данных
    priority: int = Field(3, ge=1, le=5)
    is_done: bool = False
    created_at: datetime = Field(default_factory=datetime.now)


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(..., min_length=1, max_length=100)
    text: Optional[str] = Field(None, max_length=500)
    priority: Optional[int] = Field(3, ge=1, le=5)
    is_done: Optional[bool] = False


class UserLogin(BaseModel):
    username: str = Field(..., min_length=5, max_length=20)
    password: str = Field(..., min_length=5, max_length=20)