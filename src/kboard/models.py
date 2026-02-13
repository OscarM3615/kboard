from collections import defaultdict
from datetime import date
import datetime
from typing import overload
from rich import box
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .config import STATUS_COLOURS, STATUS_NAMES
from .enums import Priority, Status


class Base(DeclarativeBase):
    ...


class Board(Base):
    __tablename__ = 'boards'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    tasks: Mapped[list['Task']] = relationship(back_populates='board',
                                               cascade='all, delete',
                                               passive_deletes=True)

    def __rich__(self) -> RenderableType:
        """Display board as a Kanban table.

        :return: rich renderable object
        """
        statuses = defaultdict(list)

        for task in self.tasks:
            statuses[task.status].append(task)

        table = Table(title=self.name, box=box.DOUBLE, expand=True)

        for s in Status:
            table.add_column(
                f'[{STATUS_COLOURS[s]}]{STATUS_NAMES[s]}[/] ({len(statuses[s])})',
                ratio=1
            )

        table.add_row(*[Group(*statuses[s]) for s in Status])

        return table

    def inline(self) -> RenderableType:
        return f'\\[[cyan]{self.id}[/]] {self.name} ({len(self.tasks)})'


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    priority: Mapped[Priority]
    tag: Mapped[str] = mapped_column(default='')
    status: Mapped[Status] = mapped_column(default=Status.TO_DO)
    due_date: Mapped[date | None]
    board_id: Mapped[int | None] = mapped_column(
        ForeignKey('boards.id', ondelete='CASCADE'))

    board: Mapped[Board | None] = relationship(back_populates='tasks')

    def __rich__(self) -> RenderableType:
        """Display task as a Kanban card.

        :return: rich renderable object
        """
        content = self.title

        if self.priority == Priority.LOW:
            content = f'[bright_black]{content}[/]'
        elif self.priority == Priority.HIGH:
            content = f'[yellow]\\[!][/] {content}'

        if self.tag:
            content += f' ([cyan]{self.tag}[/])'

        if self.due_date:
            today = date.today()

            if self.status == Status.COMPLETED or self.due_date > today:
                due_colour = 'default'
            elif self.due_date == today:
                due_colour = 'yellow'
            else:
                due_colour = 'red'
            subtitle = f'[{due_colour}]{self.due_date}[/]'
        else:
            subtitle = None

        return Panel(content, title=str(self.id), title_align='left',
                     border_style=STATUS_COLOURS[self.status],
                     subtitle=subtitle, subtitle_align='right')

    @overload
    def update(self, *, title: str | None = None,
               priority: Priority | None = None, tag: str | None = None,
               status: Status | None = None) -> None:
        """Update multiple instance attributes in a single call.

        To skip a field leave is as ``None``.

        :param title: new title
        :param priority: new priority
        :param tag: new tag
        :param status: new status
        """
        ...

    @overload
    def update(self, **kwargs) -> None:
        ...

    def update(self, **kwargs) -> None:
        for attr, value in kwargs.items():
            if value is not None:
                setattr(self, attr, value)
