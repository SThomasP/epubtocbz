from enum import Enum


class Position(Enum):
    UNKNOWN = 1
    LEFT = 2
    RIGHT = 3


class ReadingDirection(Enum):
    UNKNOWN = 1
    LTR = 2
    RTL = 3
