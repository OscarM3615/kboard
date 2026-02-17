"""This module exports the service class for the Task model.
"""

from datetime import datetime

from ..exceptions import BoardNotFoundError, TaskNotFoundError
from ..enums import Priority, Status
from ..models import Task
from ..repos.board_repo import BoardRepository
from ..repos.task_repo import TaskRepository


class TaskService:
    """Application service responsible for task-related use cases.

    This class implements business operations involving Task entities.
    """

    def __init__(self, task_repo: TaskRepository, board_repo: BoardRepository):
        """Initialise the service with repositories.

        :param task_repo: task repository
        :param board_repo: board repository
        """
        self.task_repo = task_repo
        self.board_repo = board_repo

    def get_task(self, task_id: int) -> Task:
        """Get a Task object by ID or fail if it does not exist.

        :param task_id: task ID to search
        :raises TaskNotFoundError: if the ID does not exist
        :return: task object
        """
        task = self.task_repo.get(task_id)

        if not task:
            raise TaskNotFoundError

        return task

    def add_task(self, title: str, priority: Priority, tag: str | None,
                 due_date: datetime | None, board_id: int | None) -> Task:
        """Create a new task in the database.

        :param title: task title
        :param priority: task priority value
        :param tag: task tag
        :param due_date: task due date
        :param board_id: assigned board ID
        :raises BoardNotFoundError: if the board ID does not exist
        :return: task object
        """
        board = None

        if board_id is not None:
            board = self.board_repo.get(board_id)
            if not board:
                raise BoardNotFoundError

        task = Task(title=title, priority=priority, tag=tag, due_date=due_date,
                    board=board)

        self.task_repo.add(task)

        return task

    def edit_task(self, task_id: int, title: str | None,
                  priority: Priority | None, tag: str | None,
                  due_date: datetime | None, board_id: int | None) -> Task:
        """Edit task attributes in the database.

        :param task_id: task ID to search
        :param title: new title
        :param priority: new priority
        :param tag: new tag
        :param due_date: new due date
        :param board_id: new board ID, None to omit, -1 to unassign
        :raises TaskNotFoundError: if the task ID does not exist
        :raises BoardNotFoundError: if the board ID does not exist
        :return: task object
        """
        task = self.get_task(task_id)

        task.update(title=title, priority=priority, tag=tag, due_date=due_date)

        if board_id is not None:
            if board_id == -1:
                task.board = None
            else:
                board = self.board_repo.get(board_id)
                if not board:
                    raise BoardNotFoundError
                task.board = board

        return task

    def move_task(self, task_id: int, steps: int):
        """Update a task status by a number of steps.

        :param task_id: task ID to search
        :param steps: number of steps
        :raises TaskNotFoundError: if the task ID does not exist
        :raises ValueError: if the amount of steps result in an invalid status
        :return: task object
        """
        task = self.get_task(task_id)

        try:
            task.status = Status(task.status + steps)
        except ValueError:
            raise ValueError('Invalid status movement')

        return task

    def delete_task(self, task_id: int):
        """Remove a task from the database.

        :param task_id: task ID to search
        :raises TaskNotFoundError: if the task ID does not exist
        :return: task object
        """
        task = self.get_task(task_id)

        self.task_repo.delete(task)

        return task

    def get_backlog(self):
        """Return a list of unassigned tasks.

        :return: list of tasks.
        """
        return self.task_repo.list_backlog()
