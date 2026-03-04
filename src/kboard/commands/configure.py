"""Commands related to app configuration.
"""

import typer

from ..common.message_renderer import MessageRenderer
from ..console import console
from ..db.init import init_db


app = typer.Typer()


@app.command()
def configure():
    """Create and initialise data file.
    """
    init_db()

    console.print(MessageRenderer.success('Data file created successfully.'))
