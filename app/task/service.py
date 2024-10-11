import uuid
from sqlalchemy.orm import Session
from .model import Task
from .validator import TaskCreateModel, TaskUpdateModel

class TaskService:
    @staticmethod
    def get_all(session: Session):
        tasks = session.query(Task).filter(Task.is_active == True).all()
        return [
            {
                "id": str(task.id),
                "title": str(task.title),
                "description": task.description,
            }
            for task in tasks
        ]

    @staticmethod
    def create(session: Session, data: TaskCreateModel):
        task = Task(
            id=uuid.uuid4(),
            description=data.description,
            title=data.title,
        )
        session.add(task)
        session.commit()
        return "Task created successfully"

    @staticmethod
    def update(session: Session, data: TaskUpdateModel, id: str):
        note = session.query(Task).filter(Task.id == id, Task.is_active == True).first()

        if not note:
            raise ValueError("Task not found")

        # Update fields only if provided
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(note, field, value)

        session.commit()
        return "Task updated successfully"

    @staticmethod
    def delete(session: Session, id: str):
        task = session.query(Task).filter(Task.id == id, Task.is_active == True).first()

        if not task:
            raise ValueError("Task not found")

        task.is_active = False  # Soft delete
        session.commit()
        return "Task deleted successfully"
