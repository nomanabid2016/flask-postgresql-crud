from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .model import Task


class TaskSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        fields = ("title", "description")