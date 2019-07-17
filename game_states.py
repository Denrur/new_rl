from enum import auto, Enum


class GameStates(Enum):
    MENU = auto()
    SESSION = auto()


class EntityStates(Enum):
    IDLE = auto()
    SHOW_INVENTORY = auto()
    DROP_INVENTORY = auto()
    TARGETING = auto()
    PASS_TURN = auto()
    DEAD = auto()
