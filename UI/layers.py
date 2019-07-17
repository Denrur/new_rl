from enum import Enum
from bearlibterminal import terminal as blt


class Layers(Enum):
    MAP = 0
    UI_BACKGROUND = 1
    UI_FOREGROUND = 2
    UI_TEXT = 3
    VFX_BACKGROUND = 4
    VFX_FOREGROUND = 5


def change_layer(layer):
    blt.layer(layer.value)
