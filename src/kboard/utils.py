from rich import print
from rich.panel import Panel

from .commands.backlog import backlog
from .models import Board


def success(message: str) -> None:
    """Display a success message.

    :param message: message to display
    """
    print(Panel(message, title='Success', title_align='left',
                border_style='green'))


def error(message: str) -> None:
    """Display an error message.

    :param message: Message to display.
    """
    print(Panel(message, title='Error', title_align='left', border_style='red'))

def print_result_board(board: Board | None) -> None:
    """Print the resulting board or fallback to the backlog.

    :param board: board to print
    """
    if board:
        print(board)
    else:
        backlog()
