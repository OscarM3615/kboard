"""Application CLI entry point.
"""

import typer

from .commands import backlog, board, configure, task


app = typer.Typer(no_args_is_help=True,
                  context_settings={'help_option_names': ['-h', '--help']})

app.add_typer(configure.app)
app.add_typer(backlog.app)
app.add_typer(board.app)
app.add_typer(task.app)


if __name__ == '__main__':
    app()
