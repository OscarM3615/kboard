"""Global app settings and constants.
"""

import os
from pathlib import Path

from .enums import Status


DB_PATH = Path(os.environ.get('KBOARD_HOME', Path.home())) / '.kboard.db'
"""Location to the SQLite file.
"""

STATUS_NAMES: dict[Status, str] = {
    Status.TO_DO: 'To do',
    Status.IN_PROGRESS: 'In progress',
    Status.REVIEW: 'Review',
    Status.COMPLETED: 'Completed',
}
"""Display name for each status."""

STATUS_COLOURS: dict[Status, str] = {
    Status.TO_DO: 'white',
    Status.IN_PROGRESS: 'blue',
    Status.REVIEW: 'magenta',
    Status.COMPLETED: 'green',
}
"""Display colour for each status."""
