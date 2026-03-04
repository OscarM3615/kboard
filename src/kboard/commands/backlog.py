"""Commands related to the Kanban tasks backlog.
"""

from sqlalchemy.orm import Session
import typer

from ..board.renderer import BoardRenderer
from ..console import console
from ..container import Container
from ..db.engine import engine


app = typer.Typer()


@app.command()
def backlog():
    """Display tasks from backlog.

    The backlog is composed of tasks with no assigned board.
    """
    with Session(engine) as session:
        container = Container(session)

        tasks = container.task_service.get_backlog()

        console.clear()
        console.print(BoardRenderer.kanban_from_tasks('Backlog', list(tasks)))
