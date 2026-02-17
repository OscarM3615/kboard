from datetime import datetime

from ..exceptions import BoardNotFoundError, TaskNotFoundError
from ..enums import Priority, Status
from ..models import Task
from ..repos.board_repo import BoardRepository
from ..repos.task_repo import TaskRepository


class TaskService:
    def __init__(self, task_repo: TaskRepository, board_repo: BoardRepository):
        self.task_repo = task_repo
        self.board_repo = board_repo

    def get_task(self, task_id: int) -> Task:
        task = self.task_repo.get(task_id)

        if not task:
            raise TaskNotFoundError

        return task

    def add_task(self, title: str, priority: Priority, tag: str | None,
                 due_date: datetime | None, board_id: int | None) -> Task:
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
        task = self.get_task(task_id)

        try:
            task.status = Status(task.status + steps)
        except ValueError:
            raise ValueError('Invalid status movement')

        return task

    def delete_task(self, task_id: int):
        task = self.get_task(task_id)

        self.task_repo.delete(task)

        return task

    def get_backlog(self):
        return self.task_repo.list_backlog()
