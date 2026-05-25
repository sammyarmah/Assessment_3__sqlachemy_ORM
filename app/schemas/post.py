from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str = Field(min_length=5, max_length=255)
    content: str = Field(min_length=1)
    image_filename: Optional[str] = None

class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=5, max_length=255)
    content: Optional[str] = Field(default=None, min_length=1)
    image_filename: Optional[str] = Field(default=None, max_length=255)

class PostRead(PostBase):
    id: int
    likes: int
    owner_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

