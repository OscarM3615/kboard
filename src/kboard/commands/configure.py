import typer

from ..config import engine
from ..models import Base
from ..utils import success


app = typer.Typer()


@app.command()
def configure():
    """Create and initialise data file.
    """
    Base.metadata.create_all(engine)

    success('Data file created successfully.')
