import typer

from ..console import console
from ..db.init import init_db
from ..renderers.message_renderer import MessageRenderer


app = typer.Typer()


@app.command()
def configure():
    """Create and initialise data file.
    """
    init_db()

    console.print(MessageRenderer.success('Data file created successfully.'))
