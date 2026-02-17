from typing import Annotated

import typer
from rich import print
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from ..config import engine
from ..models import Board, Status, Task
from ..utils import success, error
from ..views import BoardRenderer


app = typer.Typer(name='board', help='Manage boards.', no_args_is_help=True)


@app.command()
def ls():
    """List existing boards.
    """
    with Session(engine) as session:
        boards = session.execute(select(Board)).scalars().all()

        print(BoardRenderer.to_list(boards))


@app.command()
def add(name: Annotated[str, typer.Argument(help='Board name.')]):
    """Create a new board.
    """
    board = Board(name=name)

    with Session(engine) as session:
        session.add(board)
        session.commit()

        success(f'Created board "{board.name}" ({board.id}).')


@app.command(help='Rename a board.')
def rename(id: Annotated[int, typer.Argument(help='Board ID.')],
           name: Annotated[str, typer.Argument(help='New name.')]):
    """Rename a board.
    """
    with Session(engine) as session:
        board = session.get(Board, id)

        if not board:
            return error('Board not found.')

        board.name = name
        session.commit()

        success(f'Renamed board to "{board.name}".')


@app.command()
def rm(id: Annotated[int, typer.Argument(help='Board ID.')],
       force: Annotated[bool, typer.Option(
           '--force', '-f',
           prompt='Are you sure you want to delete the board?',
           help='Force deletion without confirmation.')] = False):
    """Delete existing board.

    If --force is not used, will ask for confirmation.
    """
    if force:
        with Session(engine) as session:
            board = session.get(Board, id)

            if not board:
                return error('Board not found.')

            session.delete(board)
            session.commit()

            success(f'Deleted board "{board.name}".')


@app.command()
def show(id: Annotated[int, typer.Argument(help='Board ID.')]):
    """Display board and its tasks.
    """
    with Session(engine) as session:
        board = session.get(Board, id)

        if not board:
            return error('Board not found.')

        print(BoardRenderer.to_kanban(board))


@app.command()
def clean(id: Annotated[int, typer.Argument(help='Board ID.')],
          force: Annotated[bool, typer.Option(
              '--force', '-f',
              prompt='Are you sure you want to delete completed tasks?',
              help='Force deletion without confirmation.', )] = False):
    """Delete completed tasks from a board.

    If --force is not used, will ask for confirmation.
    """
    if force:
        with Session(engine) as session:
            board = session.get(Board, id)

            if not board:
                return error('Board not found.')

            session.execute(delete(Task).where(Task.board_id == board.id,
                                               Task.status == Status.COMPLETED))
            session.commit()

            print(BoardRenderer.to_kanban(board))
