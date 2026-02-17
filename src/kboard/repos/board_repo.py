from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Board


class BoardRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> Sequence[Board]:
        return self.session.execute(select(Board)).scalars().all()

    def get(self, board_id: int) -> Board | None:
        return self.session.get(Board, board_id)

    def add(self, board: Board) -> None:
        self.session.add(board)

    def delete(self, board: Board) -> None:
        self.session.delete(board)
