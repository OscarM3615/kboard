"""Database-related utility functions.
"""

from .engine import engine
from ..models import Base


def init_db() -> None:
    """Create the database file and create all the tables.
    """
    Base.metadata.create_all(engine)
