"""This module exports the renderer class for board objects and their variants.
"""

from collections import defaultdict
from collections.abc import Sequence

from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .task_renderer import TaskRenderer
from ..config import STATUS_COLOURS, STATUS_NAMES
from ..enums import Status
from ..models import Board, Task


class BoardRenderer:
    """Class responsible for defining how a board should be displayed.
    """

    @staticmethod
    def _create_base_table(title: str, *, board_column: bool = False) -> Table:
        """Generate an empty rich table object.

        :param title: table name
        :param board_column: whether to include board column or not
        :return: table object
        """
        table = Table(title=title, box=box.DOUBLE, expand=True,
                      show_lines=True)

        if board_column:
            table.add_column('Board')

        for s in Status:
            table.add_column(
                f'[{STATUS_COLOURS[s]}]{STATUS_NAMES[s]}[/]',
                ratio=1
            )

        return table

    @staticmethod
    def _group_tasks_by_status(tasks: Sequence[Task]) -> dict[Status, list[Task]]:
        """Return the tasks grouped by status.

        :param tasks: list of tasks to group
        :return: mapping of status and tasks
        """
        groups = defaultdict(list)

        for task in tasks:
            groups[task.status].append(task)

        return groups

    @classmethod
    def to_kanban(cls, board: Board) -> Table:
        """Return a rich table to display a Kanban board from a board object.

        :param board: board object
        :return: rich table
        """
        statuses = cls._group_tasks_by_status(board.tasks)

        table = cls._create_base_table(f'\\[{board.id}] {board.name}')

        table.add_row(*[
            Group(*(TaskRenderer.to_panel(t) for t in statuses[s]))
            for s in Status
        ])

        return table

    @classmethod
    def to_kanban_swimlanes(cls, boards: Sequence[Board]) -> Table:
        """Return a rich table to display a Kanban board from multiple board
        objects.

        :param boards: list of board objects
        :return: rich table
        """
        table = cls._create_base_table('All active work', board_column=True)

        for board in boards:
            statuses = cls._group_tasks_by_status(board.tasks)

            table.add_row(
                Text(f'\n[{board.id}] {board.name}', style='cyan',
                     no_wrap=True),
                *[
                    Group(*(TaskRenderer.to_panel(t) for t in statuses[s]))
                    for s in Status
                ]
            )

        return table

    @classmethod
    def kanban_from_tasks(cls, title: str, tasks: Sequence['Task']) -> Table:
        """Generate a rich table to display a Kanban board from a list of tasks.

        :param title: table title
        :param tasks: list of tasks to include
        :return: rich table
        """
        table = cls._create_base_table(title)
        statuses = cls._group_tasks_by_status(tasks)

        table.add_row(*[
            Group(*(TaskRenderer.to_panel(t) for t in statuses[s]))
            for s in Status
        ])

        return table
