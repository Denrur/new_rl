from bearlibterminal import terminal as blt


def get_constants():
    screen_width = blt.state(blt.TK_WIDTH)
    screen_height = blt.state(blt.TK_HEIGHT)
    map_width = int(blt.get("ini.Game.map_width"))
    map_height = int(blt.get("ini.Game.map_height"))
    camera_width = int(blt.get("ini.Game.camera_width"))
    camera_height = int(blt.get("ini.Game.camera_height"))
    constants = {
        'screen_width': screen_width,
        'screen_height': screen_height,
        'map_width': map_width,
        'map_height': map_height,
        'camera_width': camera_width,
        'camera_height': camera_height,

    }

    return constants
