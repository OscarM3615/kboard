from rich import print
from rich.panel import Panel


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
