"""This module defines the repository class for the Board model.
"""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Board


class BoardRepository:
    """Repository responsible for persistence operations related to Board
    entities.
    """

    def __init__(self, session: Session):
        """Initialise the repository with a database session.

        :param session: SQLAlchemy session
        """
        self.session = session

    def list_all(self) -> Sequence[Board]:
        """Return a list of all the boards in the database.

        :return: list of boards
        """
        return self.session.execute(select(Board)).scalars().all()

    def get(self, board_id: int) -> Board | None:
        """Retrieve a board object by its ID if it exists.

        :param board_id: id to search
        :return: board object or None
        """
        return self.session.get(Board, board_id)

    def add(self, board: Board) -> None:
        """Add a new board to the session.

        :param board: board object
        """
        self.session.add(board)

    def delete(self, board: Board) -> None:
        """Delete a board from the session.

        :param board: board to delete
        """
        self.session.delete(board)
