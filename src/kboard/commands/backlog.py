"""Commands related to the Kanban tasks backlog.
"""

from sqlalchemy.orm import Session
import typer

from ..board.renderer import BoardRenderer
from ..board.repository import BoardRepository
from ..console import console
from ..db.engine import engine
from ..task.repository import TaskRepository
from ..task.service import TaskService


app = typer.Typer()


@app.command()
def backlog():
    """Display tasks from backlog.

    The backlog is composed of tasks with no assigned board.
    """
    with Session(engine) as session:
        task_repo = TaskRepository(session)
        board_repo = BoardRepository(session)
        service = TaskService(task_repo, board_repo)

        tasks = service.get_backlog()

        console.clear()
        console.print(BoardRenderer.kanban_from_tasks('Backlog', list(tasks)))
