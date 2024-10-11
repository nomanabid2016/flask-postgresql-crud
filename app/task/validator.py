from typing import Optional

from pydantic import (
    UUID4,
    BaseModel
)

class TaskCreateModel(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
  

