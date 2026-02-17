import typer

from ..db.init import init_db
from ..utils import success


app = typer.Typer()


@app.command()
def configure():
    """Create and initialise data file.
    """
    init_db()

    success('Data file created successfully.')
