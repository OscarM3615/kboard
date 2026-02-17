"""This module exports the renderer class for status messages.
"""

from rich.panel import Panel


class MessageRenderer:
    """Renderer class to generate rich printable status messages.
    """

    @staticmethod
    def success(message: str) -> Panel:
        """Generate a success message.

        :param message: panel content
        :return: panel object
        """
        return Panel(message, title='Success', title_align='left',
                     border_style='green')

    @staticmethod
    def error(message: str) -> Panel:
        """Generate an error message.

        :param message: panel content
        :return: panel object
        """
        return Panel(message, title='Error', title_align='left',
                     border_style='red')
