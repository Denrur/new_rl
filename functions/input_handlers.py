from bearlibterminal import terminal as blt
from game_states import EntityStates


def handle_keys(entity, key):
    if entity.state in (EntityStates.SHOW_INVENTORY, EntityStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif entity.state == EntityStates.TARGETING:
        return handle_targeting_keys(key)
    elif entity.state == EntityStates.DEAD:
        return handle_menu_keys(key)
    elif entity.state == EntityStates.IDLE:
        return handle_player_turn_keys(key)
    else:
        return {}


def handle_player_turn_keys(key):
    if key == blt.TK_UP or key == blt.TK_W:
        return {'move': (0, -1)}
    elif key == blt.TK_DOWN or key == blt.TK_X:
        return {'move': (0, 1)}
    elif key == blt.TK_LEFT or key == blt.TK_A:
        return {'move': (-1, 0)}
    elif key == blt.TK_RIGHT or key == blt.TK_D:
        return {'move': (1, 0)}
    elif key == blt.TK_Q:
        return {'move': (-1, -1)}
    elif key == blt.TK_E:
        return {'move': (1, -1)}
    elif key == blt.TK_Z:
        return {'move': (-1, 1)}
    elif key == blt.TK_C:
        return {'move': (1, 1)}

    if key == blt.TK_G:
        return {'pickup': True}

    if key == blt.TK_MOUSE_SCROLL:
        return{'scroll': True}
    # elif key == blt.TK_O:
    #     return{'scroll_up': True}
    # elif key == blt.TK_L:
    #     return{'scroll_down': True}

    if key == blt.TK_G:
        return{'pickup': True}

    elif key == blt.TK_I:
        return{'show_inventory': True}

    elif key == blt.TK_O:
        return{'drop_inventory': True}

    if key == blt.TK_RETURN and blt.TK_ALT:
        return {'fullscreen': True}
    elif key == blt.TK_ESCAPE:
        return {'exit': True}

    if key == 133:
        return {'mouse': True}
    return {}


def handle_targeting_keys(key):
    if key == blt.TK_ESCAPE:
        return {'exit': True}

    if key == blt.TK_MOUSE_LEFT:
        x = blt.state(blt.TK_MOUSE_X)
        y = blt.state(blt.TK_MOUSE_Y)
        return {'left_click': (x, y)}
    elif key == blt.TK_MOUSE_RIGHT:
        x = blt.state(blt.TK_MOUSE_X)
        y = blt.state(blt.TK_MOUSE_Y)
        return {'right_click': (x, y)}

    return {}


def handle_inventory_keys(key):
    index = key - 4

    if key == blt.TK_ESCAPE:
        return {'exit': True}
    elif index >= 0:
        return {'inventory_index': index}

    return {}


def handle_menu_keys(key):
    if key == blt.TK_RETURN and blt.TK_ALT:
        return {'fullscreen': True}
    elif key == blt.TK_ESCAPE:
        return {'exit': True}
    if key == 133:
        return {'mouse': True}

    return {}


def handle_player_dead_key(key):
    if key == blt.TK_RETURN and blt.TK_ALT:
        return {'fullscreen': True}
    elif key == blt.TK_ESCAPE:
        return {'exit': True}

    if key == blt.TK_I:
        return {'show_inventory': True}

    if key == 133:
        return {'mouse': True}

    return {}


def handle_main_menu():
    code = blt.read()

    if code == blt.TK_A:
        return {'new_game': True}
    elif code == blt.TK_B:
        return{'load_game': True}
    elif code == blt.TK_C or code == blt.TK_ESCAPE:
        return {'exit': True}

    return {}