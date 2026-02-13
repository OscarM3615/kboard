from rich import print
from sqlalchemy import select
from sqlalchemy.orm import Session
import typer

from ..config import engine
from ..models import Board, Task


app = typer.Typer()


@app.command()
def backlog():
    """Display tasks from backlog.

    The backlog is composed of tasks with no assigned board.
    """
    with Session(engine) as session:
        tasks = session.execute(
            select(Task).where(Task.board_id == None)).scalars().all()

        board = Board(name='Backlog', tasks=tasks)

        print(board)
