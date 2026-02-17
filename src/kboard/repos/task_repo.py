from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from ..enums import Status
from ..models import Task


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def add(self, task: Task) -> None:
        self.session.add(task)

    def delete(self, task: Task) -> None:
        self.session.delete(task)

    def list_backlog(self) -> Sequence[Task]:
        return self.session.execute(
            select(Task).where(Task.board_id.is_(None))
        ).scalars().all()

    def delete_completed_from_board(self, board_id: int) -> None:
        self.session.execute(
            delete(Task).where(Task.board_id == board_id,
                               Task.status == Status.COMPLETED)
        )
