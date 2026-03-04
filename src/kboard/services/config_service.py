"""This module exports the service class for the Task model.
"""


from ..repos.config_repo import ConfigRepository


class ConfigService:
    """Application service responsible for config-related use cases.

    This class implements configuration get/set operations.
    """

    LAST_VIEW = 'last_view'

    def __init__(self, repo: ConfigRepository):
        """Initialise the service with repositories.

        :param repo: the config repo
        """
        self.repo = repo

    def get_last_view(self) -> str:
        """Retrieve the last view value.

        :return: last view value
        """
        value = self.repo.get(self.LAST_VIEW)

        return value or 'all'

    def set_last_view_all(self) -> None:
        """Indicate that the user last viewed all boards.
        """
        self.repo.set(self.LAST_VIEW, 'all')

    def set_last_view_board(self) -> None:
        """Indicate that the user last viewed a single board.
        """
        self.repo.set(self.LAST_VIEW, 'board')
