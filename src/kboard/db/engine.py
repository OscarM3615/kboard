"""This module exports a single instance to the database engine.
"""

from sqlalchemy import create_engine

from ..config import DB_PATH


engine = create_engine(f'sqlite:///{DB_PATH}')
"""Database engine."""
