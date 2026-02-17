from sqlalchemy import create_engine

from ..config import DB_PATH


engine = create_engine(f'sqlite:///{DB_PATH}')
