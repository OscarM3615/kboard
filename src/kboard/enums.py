from enum import Enum


class Priority(int, Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3


class Status(int, Enum):
    TO_DO = 1
    IN_PROGRESS = 2
    REVIEW = 3
    COMPLETED = 4
