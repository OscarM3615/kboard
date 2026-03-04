"""This module defines the repository class for the Task model.
"""

from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from ..enums import Status
from ..models import Task


class TaskRepository:
    """Repository responsible for persistence operations related to Task
    entities.
    """

    def __init__(self, session: Session):
        """Initialise the repository with a database session.

        :param session: SQLAlchemy session
        """
        self.session = session

    def get(self, task_id: int) -> Task | None:
        """Retrieve a task object by its ID if it exists.

        :param task_id: id to search
        :return: task object or None
        """
        return self.session.get(Task, task_id)

    def add(self, task: Task) -> None:
        """Add a new task to the session.

        :param task: task object
        """
        self.session.add(task)

    def delete(self, task: Task) -> None:
        """Delete a task from the session.

        :param task: task to delete
        """
        self.session.delete(task)

    def list_backlog(self) -> Sequence[Task]:
        """Return a list of unassigned tasks.

        :return: list of tasks
        """
        return self.session.execute(
            select(Task).where(Task.board_id.is_(None))
        ).scalars().all()

    def delete_completed_from_board(self, board_id: int) -> None:
        """Delete completed tasks from the database.

        :param board_id: board ID to clear
        """
        self.session.execute(
            delete(Task).where(Task.board_id == board_id,
                               Task.status == Status.COMPLETED)
        )
