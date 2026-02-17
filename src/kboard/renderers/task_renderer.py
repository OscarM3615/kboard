"""This module exports the renderer class for task objects.
"""

from datetime import date

from rich.panel import Panel

from ..config import STATUS_COLOURS
from ..enums import Priority, Status
from ..models import Task


class TaskRenderer:
    """Class responsible for defining how a task should be displayed.
    """

    @staticmethod
    def _build_subtitle(task: Task) -> str | None:
        """Helper function to generate the subtitle of a task panel.

        :param task: task object
        :return: subtitle as string
        """
        if not task.due_date:
            return None

        today = date.today()

        if task.status == Status.COMPLETED or task.due_date > today:
            colour = 'default'
        elif task.due_date == today:
            colour = 'yellow'
        else:
            colour = 'red'

        return f'[{colour}]{task.due_date}[/]'

    @classmethod
    def to_panel(cls, task: Task) -> Panel:
        """Generate a rich displayable panel representing a Kanban task.

        :param task: task object
        :return: rich panel
        """
        content = task.title

        if task.priority == Priority.LOW:
            content = f'[bright_black]{content}[/]'
        elif task.priority == Priority.HIGH:
            content = f'[yellow]\\[!][/] {content}'

        if task.tag:
            content += f' ([cyan]{task.tag}[/])'

        subtitle = cls._build_subtitle(task)

        return Panel(content, title=str(task.id), title_align='left',
                     border_style=STATUS_COLOURS[task.status],
                     subtitle=subtitle, subtitle_align='right')
