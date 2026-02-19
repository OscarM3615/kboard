"""Commands related to the Kanban tasks backlog.
"""

from sqlalchemy.orm import Session
import typer

from ..console import console
from ..db.engine import engine
from ..renderers.board_renderer import BoardRenderer
from ..repos.board_repo import BoardRepository
from ..repos.task_repo import TaskRepository
from ..services.task_service import TaskService


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
