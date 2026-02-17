from rich.panel import Panel


class MessageRenderer:
    @staticmethod
    def success(message: str) -> Panel:
        return Panel(message, title='Success', title_align='left',
                     border_style='green')

    @staticmethod
    def error(message: str) -> Panel:
        return Panel(message, title='Error', title_align='left',
                     border_style='red')
