"""This module defines the enums to be used by database models or CLI
interfaces.
"""

from enum import Enum


class Priority(int, Enum):
    """Task priority.
    """

    LOW = 1
    NORMAL = 2
    HIGH = 3


class Status(int, Enum):
    """Task status.
    """

    TO_DO = 1
    IN_PROGRESS = 2
    REVIEW = 3
    COMPLETED = 4
