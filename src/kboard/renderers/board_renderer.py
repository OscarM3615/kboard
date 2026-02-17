from collections import defaultdict
from collections.abc import Sequence

from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.table import Table

from .task_renderer import TaskRenderer
from ..config import STATUS_COLOURS, STATUS_NAMES
from ..enums import Status
from ..models import Board, Task


class BoardRenderer:
    @staticmethod
    def _create_base_table(title: str) -> Table:
        table = Table(title=title, box=box.DOUBLE, expand=True)

        for s in Status:
            table.add_column(
                f'[{STATUS_COLOURS[s]}]{STATUS_NAMES[s]}[/]',
                ratio=1
            )

        return table

    @staticmethod
    def _group_tasks_by_status(tasks: list[Task]) -> dict[Status, list[Task]]:
        groups = defaultdict(list)

        for task in tasks:
            groups[task.status].append(task)

        return groups

    @classmethod
    def to_kanban(cls, board: Board) -> Table:
        statuses = cls._group_tasks_by_status(board.tasks)

        table = cls._create_base_table(board.name)

        table.add_row(*[
            Group(*(TaskRenderer.to_panel(t) for t in statuses[s]))
            for s in Status
        ])

        return table

    @staticmethod
    def _inline(board: Board) -> str:
        return (f'\\[[cyan]{board.id}[/]] {board.name}'
                f' ({board.active_task_count})')

    @classmethod
    def to_list(cls, boards: Sequence[Board]) -> Panel:
        titles = [cls._inline(b) for b in boards]

        return Panel(Group(*titles), title='Boards', title_align='left',
                     border_style='blue')

    @classmethod
    def kanban_from_tasks(cls, title: str, tasks: list['Task']) -> Table:
        table = cls._create_base_table(title)
        statuses = cls._group_tasks_by_status(tasks)

        table.add_row(*[
            Group(*(TaskRenderer.to_panel(t) for t in statuses[s]))
            for s in Status
        ])

        return table
