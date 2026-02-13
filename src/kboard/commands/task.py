from typing import Annotated

import typer
from sqlalchemy.orm import Session

from ..config import STATUS_NAMES, engine
from ..models import Board, Priority, Status, Task
from ..utils import error, success


app = typer.Typer(name='task', help='Manage tasks.', no_args_is_help=True)


@app.command()
def add(title: Annotated[str, typer.Argument(help='Task title.')],
        priority: Annotated[Priority, typer.Option(
            '--priority', '-p', help='Task priority.')] = Priority.NORMAL,
        tag: Annotated[str | None, typer.Option(
            '--tag', '-t', help='Task custom tag.',
        )] = None,
        board_id: Annotated[int | None, typer.Option(
            '--board', '-b', help='Board ID to assign to the task.')] = None):
    """Add a new task.

    The task can be preassigned to a board using the --board option.
    """
    with Session(engine) as session:
        if board_id:
            board = session.get(Board, board_id)

            if not board:
                return error('Board not found.')
        else:
            board = None

        task = Task(title=title, priority=priority, tag=tag, board=board)

        session.add(task)
        session.commit()

        success(f'Created task with ID {task.id}.')


@app.command()
def edit(id: Annotated[int, typer.Argument(help='Task ID.')],
         title: Annotated[str | None, typer.Option(
             '--title', help='New task title.')] = None,
         priority: Annotated[Priority | None, typer.Option(
             '--priority', '-p', help='New task priority.')] = None,
         tag: Annotated[str | None, typer.Option(
             '--tag', '-t', help='Task custom tag.',
         )] = None,
         board_id: Annotated[int | None, typer.Option(
        '-b', '--board', help='New board ID (use -1 to unasign).')] = None):
    """Edit existing task attributes.

    All parameters and options from the `add` command are optional here.
    """
    with Session(engine) as session:
        task = session.get(Task, id)

        if not task:
            return error('Task not found.')

        new_attrs = {'title': title, 'priority': priority, 'tag': tag}
        task.update(**new_attrs)

        if board_id is not None:
            if board_id != -1:
                board = session.get(Board, board_id)

                if not board:
                    return error('Board not found.')
            else:
                board = None
            task.board = board

        session.commit()

        success(f'Updated task "{task.title}" attributes.')


@app.command()
def mv(id: Annotated[int, typer.Argument(help='Task ID.')],
       steps: Annotated[int, typer.Option(
           '--steps', '-s', help='Number of steps to move.')] = 1):
    """Move a task from its current status.

    To customise the direction or number of steps, use the --steps option.

    To move a task backwards the steps must be negative.
    """
    with Session(engine) as session:
        task = session.get(Task, id)

        if not task:
            return error('Task not found.')

        try:
            task.status = Status(task.status + steps)
        except ValueError:
            return error(f'Unable to move {steps} step(s).')

        session.commit()

        success(
            f'Moved task "{task.title}" to [cyan]{STATUS_NAMES[task.status]}[/].')


@app.command()
def rm(id: Annotated[int, typer.Argument(help='Task ID.')],
       force: Annotated[bool, typer.Option(
           '--force', '-f',
           prompt='Are you sure you want to delete the task?',
           help='Force deletion without confirmation.')] = False):
    """Delete existing task.

    If --force is not used, will ask for confirmation.
    """
    if force:
        with Session(engine) as session:
            task = session.get(Task, id)

            if not task:
                return error('Task not found.')

            session.delete(task)
            session.commit()

            success(f'Deleted task with ID {task.id}.')
