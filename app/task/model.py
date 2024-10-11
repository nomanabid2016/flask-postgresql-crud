from sqlalchemy import Column, String
from database import BaseModel

class Task(BaseModel):
    __tablename__ = "tasks"
    title = Column(String(100), nullable=False)
    description = Column(String(255))