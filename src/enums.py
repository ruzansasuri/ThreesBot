
from enum import Enum, StrEnum


class Directions(Enum):
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)

class GameState(Enum):
    ONGOING = 0
    WON = 1
    GAME_OVER = 2

class Messages(StrEnum):
    BAD_MOVE = "Invalid move! No tiles can move in that direction."
    BAD_INPUT = "Invalid input! Use l/r/u/d."