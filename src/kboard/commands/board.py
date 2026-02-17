from typing import Annotated

import typer
from sqlalchemy.orm import Session

from ..console import console
from ..db.engine import engine
from ..exceptions import BoardNotFoundError
from ..renderers.board_renderer import BoardRenderer
from ..renderers.message_renderer import MessageRenderer
from ..repos.board_repo import BoardRepository
from ..repos.task_repo import TaskRepository
from ..services.board_service import BoardService


app = typer.Typer(name='board', help='Manage boards.', no_args_is_help=True)


@app.command()
def ls():
    """List existing boards.
    """
    with Session(engine) as session:
        board_repo = BoardRepository(session)
        tasks_repo = TaskRepository(session)
        service = BoardService(board_repo, tasks_repo)

        boards = service.list_boards()

        console.print(BoardRenderer.to_list(boards))


@app.command()
def add(name: Annotated[str, typer.Argument(help='Board name.')]):
    """Create a new board.
    """
    with Session(engine) as session:
        board_repo = BoardRepository(session)
        tasks_repo = TaskRepository(session)
        service = BoardService(board_repo, tasks_repo)

        board = service.create_board(name)
        session.commit()

        console.print(MessageRenderer.success(f'Created board "{board.name}".'))


@app.command(help='Rename a board.')
def rename(id: Annotated[int, typer.Argument(help='Board ID.')],
           name: Annotated[str, typer.Argument(help='New name.')]):
    """Rename a board.
    """
    with Session(engine) as session:
        board_repo = BoardRepository(session)
        tasks_repo = TaskRepository(session)
        service = BoardService(board_repo, tasks_repo)

        try:
            board = service.rename_board(id, name)
            session.commit()
        except BoardNotFoundError:
            return console.print(MessageRenderer.error('Board not found.'))

        console.print(
            MessageRenderer.success(f'Renamed board to "{board.name}".'))


@app.command()
def rm(id: Annotated[int, typer.Argument(help='Board ID.')],
       force: Annotated[bool, typer.Option(
           '--force', '-f',
           prompt='Are you sure you want to delete the board?',
           help='Force deletion without confirmation.')] = False):
    """Delete existing board.

    If --force is not used, will ask for confirmation.
    """
    if not force:
        return

    with Session(engine) as session:
        board_repo = BoardRepository(session)
        tasks_repo = TaskRepository(session)
        service = BoardService(board_repo, tasks_repo)

        try:
            board = service.delete_board(id)
            session.commit()
        except BoardNotFoundError:
            return console.print(MessageRenderer.error('Board not found.'))

        console.print(MessageRenderer.success(f'Deleted board "{board.name}".'))


@app.command()
def show(id: Annotated[int, typer.Argument(help='Board ID.')]):
    """Display board and its tasks.
    """
    with Session(engine) as session:
        board_repo = BoardRepository(session)
        tasks_repo = TaskRepository(session)
        service = BoardService(board_repo, tasks_repo)

        try:
            board = service.get_board(id)
        except BoardNotFoundError:
            return console.print(MessageRenderer.error('Board not found.'))

        console.print(BoardRenderer.to_kanban(board))


@app.command()
def clean(id: Annotated[int, typer.Argument(help='Board ID.')],
          force: Annotated[bool, typer.Option(
              '--force', '-f',
              prompt='Are you sure you want to delete completed tasks?',
              help='Force deletion without confirmation.', )] = False):
    """Delete completed tasks from a board.

    If --force is not used, will ask for confirmation.
    """
    if not force:
        return

    with Session(engine) as session:
        board_repo = BoardRepository(session)
        tasks_repo = TaskRepository(session)
        service = BoardService(board_repo, tasks_repo)

        try:
            board = service.clean_completed_tasks(id)
            session.commit()
        except BoardNotFoundError:
            return console.print(MessageRenderer.error('Board not found.'))

        console.print(BoardRenderer.to_kanban(board))
