"""This module exports the service class to display the UI.
"""

from rich.console import RenderableType

from ..models import Board
from ..renderers.board_renderer import BoardRenderer
from ..services.board_service import BoardService
from ..services.config_service import ConfigService
from ..services.task_service import TaskService


class DisplayService:
    """Application service responsible for rendering the correct view after
    user action.
    """

    def __init__(self, config_service: ConfigService,
                 board_service: BoardService, task_service: TaskService,
                 renderer: BoardRenderer):
        """Initialise the service with its dependencies.
        """
        self.config_service = config_service
        self.board_service = board_service
        self.task_service = task_service
        self.renderer = renderer

    def get_ui_renderable(self, board: Board | None) -> RenderableType:
        """Render the UI depending on the last displayed setting (all or single
        board).
        """
        last_view = self.config_service.get_last_view()

        if last_view == 'all':
            boards = self.board_service.list_boards()

            return self.renderer.to_kanban_swimlanes(boards)

        if board is not None:
            return self.renderer.to_kanban(board)

        tasks = self.task_service.get_backlog()

        return self.renderer.kanban_from_tasks('Backlog', tasks)
