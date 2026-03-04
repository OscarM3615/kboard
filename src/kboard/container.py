"""This module exports the DI container class.
"""

from sqlalchemy.orm import Session

from .board.renderer import BoardRenderer
from .board.repository import BoardRepository
from .board.service import BoardService
from .common.display_service import DisplayService
from .config.repository import ConfigRepository
from .config.service import ConfigService
from .task.repository import TaskRepository
from .task.service import TaskService


class Container:
    """DI container responsible for wiring all the dependencies for the app
    commands.
    """

    def __init__(self, session: Session):
        """Initialise all dependencies.

        :param session: SQLAlchemy session
        """
        self.board_repo = BoardRepository(session)
        self.task_repo = TaskRepository(session)
        self.config_repo = ConfigRepository(session)

        self.renderer = BoardRenderer()

        self.board_service = BoardService(self.board_repo, self.task_repo)
        self.task_service = TaskService(self.task_repo, self.board_repo)
        self.config_service = ConfigService(self.config_repo)
        self.display_service = DisplayService(self.config_service,
                                              self.board_service,
                                              self.task_service,
                                              self.renderer)
