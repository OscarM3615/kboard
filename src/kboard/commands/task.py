"""Commands responsible for managing tasks.
"""

from datetime import datetime
from typing import Annotated

import typer
from sqlalchemy.orm import Session

from ..console import console
from ..db.engine import engine
from ..exceptions import BoardNotFoundError, TaskNotFoundError
from ..models import Priority
from ..renderers.message_renderer import MessageRenderer
from ..renderers.board_renderer import BoardRenderer
from ..repos.board_repo import BoardRepository
from ..repos.config_repo import ConfigRepository
from ..repos.task_repo import TaskRepository
from ..services.board_service import BoardService
from ..services.config_service import ConfigService
from ..services.display_service import DisplayService
from ..services.task_service import TaskService


app = typer.Typer(name='task', help='Manage tasks.', no_args_is_help=True)


@app.command()
def add(title: Annotated[str, typer.Argument(help='Task title.')],
        priority: Annotated[Priority, typer.Option(
            '--priority', '-p', help='Task priority.')] = Priority.NORMAL,
        tag: Annotated[str | None, typer.Option(
            '--tag', '-t', help='Task custom tag.',)] = None,
        due_date: Annotated[datetime | None, typer.Option(
            '--due', '-d', help='Task due date.', formats=['%Y-%m-%d'])] = None,
        board_id: Annotated[int | None, typer.Option(
            '--board', '-b', help='Board ID to assign to the task.')] = None):
    """Add a new task.

    The task can be preassigned to a board using the --board option.
    """
    with Session(engine) as session:
        task_repo = TaskRepository(session)
        board_repo = BoardRepository(session)
        config_repo = ConfigRepository(session)

        task_service = TaskService(task_repo, board_repo)
        board_service = BoardService(board_repo, task_repo)
        config_service = ConfigService(config_repo)
        display_service = DisplayService(config_service, board_service,
                                         task_service, BoardRenderer())

        try:
            task = task_service.add_task(
                title, priority, tag, due_date, board_id)
        except BoardNotFoundError:
            return console.print(MessageRenderer.error('Board not found.'))

        session.add(task)
        session.commit()

        console.clear()
        console.print(display_service.get_ui_renderable(task.board))


@app.command()
def edit(id: Annotated[int, typer.Argument(help='Task ID.')],
         title: Annotated[str | None, typer.Option(
             '--title', help='New task title.')] = None,
         priority: Annotated[Priority | None, typer.Option(
             '--priority', '-p', help='New task priority.')] = None,
         tag: Annotated[str | None, typer.Option(
             '--tag', '-t', help='Task custom tag.')] = None,
         due_date: Annotated[datetime | None, typer.Option(
             '--due', '-d', help='Task due date.', formats=['%Y-%m-%d'])] = None,
         board_id: Annotated[int | None, typer.Option(
        '-b', '--board', help='New board ID (use -1 to unasign).')] = None):
    """Edit existing task attributes.

    All parameters and options from the `add` command are optional here.
    """
    with Session(engine) as session:
        task_repo = TaskRepository(session)
        board_repo = BoardRepository(session)
        config_repo = ConfigRepository(session)

        task_service = TaskService(task_repo, board_repo)
        board_service = BoardService(board_repo, task_repo)
        config_service = ConfigService(config_repo)
        display_service = DisplayService(config_service, board_service,
                                         task_service, BoardRenderer())

        try:
            task = task_service.edit_task(id, title, priority, tag, due_date,
                                          board_id)
            session.commit()
        except TaskNotFoundError:
            return console.print(MessageRenderer.error('Task not found.'))
        except BoardNotFoundError:
            return console.print(MessageRenderer.error('Board not found.'))

        console.clear()
        console.print(display_service.get_ui_renderable(task.board))


@app.command()
def mv(id: Annotated[int, typer.Argument(help='Task ID.')],
       steps: Annotated[int, typer.Option(
           '--steps', '-s', help='Number of steps to move.')] = 1):
    """Move a task from its current status.

    To customise the direction or number of steps, use the --steps option.

    To move a task backwards the steps must be negative.
    """
    with Session(engine) as session:
        task_repo = TaskRepository(session)
        board_repo = BoardRepository(session)
        config_repo = ConfigRepository(session)

        task_service = TaskService(task_repo, board_repo)
        board_service = BoardService(board_repo, task_repo)
        config_service = ConfigService(config_repo)
        display_service = DisplayService(config_service, board_service,
                                         task_service, BoardRenderer())

        try:
            task = task_service.move_task(id, steps)
            session.commit()
        except TaskNotFoundError:
            return console.print(MessageRenderer.error('Task not found.'))
        except ValueError:
            return console.print(
                MessageRenderer.error(f'Unable to move {steps} step(s).'))

        console.clear()
        console.print(display_service.get_ui_renderable(task.board))


@app.command()
def rm(id: Annotated[int, typer.Argument(help='Task ID.')],
       force: Annotated[bool, typer.Option(
           '--force', '-f',
           prompt='Are you sure you want to delete the task?',
           help='Force deletion without confirmation.')] = False):
    """Delete existing task.

    If --force is not used, will ask for confirmation.
    """
    if not force:
        return

    with Session(engine) as session:
        task_repo = TaskRepository(session)
        board_repo = BoardRepository(session)
        config_repo = ConfigRepository(session)

        task_service = TaskService(task_repo, board_repo)
        board_service = BoardService(board_repo, task_repo)
        config_service = ConfigService(config_repo)
        display_service = DisplayService(config_service, board_service,
                                         task_service, BoardRenderer())

        try:
            task = task_service.delete_task(id)
            board = task.board
            session.commit()
        except TaskNotFoundError:
            return console.print(MessageRenderer.error('Task not found.'))

        console.clear()
        console.print(display_service.get_ui_renderable(board))
