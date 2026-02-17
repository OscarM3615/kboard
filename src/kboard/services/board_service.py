"""This module exports the service class for the Board model.
"""

from collections.abc import Sequence

from ..exceptions import BoardNotFoundError
from ..models import Board
from ..repos.board_repo import BoardRepository
from ..repos.task_repo import TaskRepository


class BoardService:
    """Application service responsible for board-related use cases.

    This class implements business operations involving Board entities.
    """

    def __init__(self, board_repo: BoardRepository, task_repo: TaskRepository):
        """Initialise the service with repositories.

        :param board_repo: board repository
        :param task_repo: task repository
        """
        self.board_repo = board_repo
        self.task_repo = task_repo

    def list_boards(self) -> Sequence[Board]:
        """Return a list of existing boards.

        :return: list of boards.
        """
        return self.board_repo.list_all()

    def get_board(self, board_id: int) -> Board:
        """Get a Board object by ID or fail if it does not exist.

        :param board_id: board ID to search
        :raises BoardNotFoundError: if the ID does not exist
        :return: board object
        """
        board = self.board_repo.get(board_id)

        if not board:
            raise BoardNotFoundError

        return board

    def create_board(self, name: str) -> Board:
        """Create a new Board object in the database.

        :param name: board name
        :return: board object
        """
        board = Board(name=name)
        self.board_repo.add(board)

        return board

    def rename_board(self, board_id: int, name: str) -> Board:
        """Update the name of a board.

        :param board_id: board ID to search
        :param name: new board name
        :return: board object
        """
        board = self.get_board(board_id)
        board.name = name

        return board

    def delete_board(self, board_id: int) -> Board:
        """Delete a board from the database.

        :param board_id: board ID to search
        :return: board object
        """
        board = self.get_board(board_id)
        self.board_repo.delete(board)

        return board

    def clean_completed_tasks(self, board_id: int) -> Board:
        """Remove all completed tasks from a board.

        :param board_id: board ID to search
        :return: board object
        """
        board = self.get_board(board_id)
        self.task_repo.delete_completed_from_board(board_id)

        return board
