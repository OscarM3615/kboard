from .engine import engine
from ..models import Base


def init_db() -> None:
    Base.metadata.create_all(engine)
