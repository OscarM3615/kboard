from collections.abc import Sequence

from ..exceptions import BoardNotFoundError
from ..models import Board
from ..repos.board_repo import BoardRepository
from ..repos.task_repo import TaskRepository


class BoardService:
    def __init__(self, board_repo: BoardRepository, task_repo: TaskRepository):
        self.board_repo = board_repo
        self.task_repo = task_repo

    def list_boards(self) -> Sequence[Board]:
        return self.board_repo.list_all()

    def get_board(self, board_id: int) -> Board:
        board = self.board_repo.get(board_id)

        if not board:
            raise BoardNotFoundError

        return board

    def create_board(self, name: str) -> Board:
        board = Board(name=name)
        self.board_repo.add(board)

        return board

    def rename_board(self, board_id: int, name: str) -> Board:
        board = self.get_board(board_id)
        board.name = name

        return board

    def delete_board(self, board_id: int) -> Board:
        board = self.get_board(board_id)
        self.board_repo.delete(board)

        return board

    def clean_completed_tasks(self, board_id: int) -> Board:
        board = self.get_board(board_id)
        self.task_repo.delete_completed_from_board(board_id)

        return board
