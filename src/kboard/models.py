"""This module declares all the database models and their relationships.
"""

from datetime import date
from typing import overload
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .enums import Priority, Status


class Base(DeclarativeBase):
    ...


class Board(Base):
    """Container for multiple tasks that represents a Kanban board.
    """

    __tablename__ = 'boards'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    tasks: Mapped[list['Task']] = relationship(back_populates='board',
                                               cascade='all, delete',
                                               passive_deletes=True)

    @property
    def active_task_count(self) -> int:
        """Count of the tasks in the board that are not completed yet.
        """
        return sum(1 for t in self.tasks if t.status != Status.COMPLETED)


class Task(Base):
    """Unit of work that can be moved across a board.
    """

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

    @overload
    def update(self, *, title: str | None = None,
               priority: Priority | None = None, tag: str | None = None,
               status: Status | None = None, due_date: date | None) -> None:
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
