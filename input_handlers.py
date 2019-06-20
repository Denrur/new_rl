from bearlibterminal import terminal as blt
from game_states import GameStates


def handle_keys(game_state, key):
    if game_state == GameStates.PLAYERS_TURN:  # GameStates.SESSION:
        return handle_sessions_keys(key)
    elif game_state == 'targeting':  # GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_menu_keys(key)
#    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
#        return handle_inventory_keys(key)
    else:
        return {}


def handle_sessions_keys(key):
    # Movement keys
    if key == blt.TK_UP or key == blt.TK_W:
        # print('Up')
        return {'move': (0, -1)}
    elif key == blt.TK_DOWN or key == blt.TK_X:
        # print('Down')
        return {'move': (0, 1)}
    elif key == blt.TK_LEFT or key == blt.TK_A:
        # print('Left')
        return {'move': (-1, 0)}
    elif key == blt.TK_RIGHT or key == blt.TK_D:
        # print('Right')
        return {'move': (1, 0)}
    elif key == blt.TK_Q:
        return {'move': (-1, -1)}
    elif key == blt.TK_E:
        return {'move': (1, -1)}
    elif key == blt.TK_Z:
        return {'move': (-1, 1)}
    elif key == blt.TK_C:
        return {'move': (1, 1)}

    if key == blt.TK_MOUSE_SCROLL:
        # Mouse wheel scroll
        return{'scroll': True}
    elif key == blt.TK_O:
        return{'scroll_up': True}
    elif key == blt.TK_L:
        return{'scroll_down': True}

    if key == blt.TK_G:
        return{'pickup': True}

    elif key == blt.TK_I:
        # print('show_inventory')
        return{'show_inventory': True}

    elif key == blt.TK_O:
        return{'drop_inventory': True}

    if key == blt.TK_RETURN and blt.TK_ALT:
        return {'fullscreen': True}

    elif key == blt.TK_ESCAPE:
        return {'exit': True}

    if key == 133:
        return {'mouse': True}
    # print("Code ", key)
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
    # print("Code ", key)
    return {}
