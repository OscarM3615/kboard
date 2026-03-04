"""This module defines the repository class for the AppConfig model.
"""

from sqlalchemy.orm import Session

from ..models import AppConfig


class ConfigRepository:
    """Repository responsible for persistence operations related to AppConfig
    entities.
    """


    def __init__(self, session: Session):
        """Initialise the repository with a database session.

        :param session: SQLAlchemy session
        """
        self.session = session

    def get(self, key: str) -> str | None:
        """Retrieve a config value.

        :param key: config key
        :return: config value
        """
        config = self.session.get(AppConfig, key)

        return config.value if config else None

    def set(self, key: str, value: str) -> None:
        """Set a new value to a config param.

        :param key: config key
        :param value: config value
        """
        config = self.session.get(AppConfig, key)

        if not config:
            config = AppConfig(key=key, value=value)
            self.session.add(config)
        else:
            config.value = value

        self.session.commit()
