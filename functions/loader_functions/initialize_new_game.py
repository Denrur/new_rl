from bearlibterminal import terminal as blt
from camera import Camera
from components.equipment import Equipment, EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Entity
from components.fov import Fov
from UI.game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from map_objects.map_generator import generate_map


def get_constants():
    screen_width = blt.state(blt.TK_WIDTH)
    screen_height = blt.state(blt.TK_HEIGHT)
    map_width = int(blt.get("ini.Game.map_width"))
    map_height = int(blt.get("ini.Game.map_height"))
    camera_width = int(screen_width * 3 / 4)  # int(blt.get("ini.Game.camera_width"))
    camera_height = int(screen_height * 3 / 4)  # int(blt.get("ini.Game.camera_height"))
    constants = {
        'screen_width': screen_width,
        'screen_height': screen_height,
        'map_width': map_width,
        'map_height': map_height,
        'camera_width': camera_width,
        'camera_height': camera_height,

    }

    return constants


def get_game_variables(constants):
    fighter_component = Fighter(hp=3000, defense=2, power=5)
    inventory_component = Inventory(26)
    game_map = GameMap(constants['map_width'], constants['map_height'])
    fov_component = Fov(game_map)
    equipment_component = Equipment()
    player = Entity(0, 0,
                    '@', 'You', 'white', game_map.entities,
                    fighter=fighter_component,
                    fov=fov_component,
                    inventory=inventory_component,
                    equipment=equipment_component)

    equippable_component = Equippable(EquipmentSlots.RIGHT_HAND, power_bonus=2)
    dagger = Entity(0, 0, '-', 'Dagger', 'blue', game_map.items,
                    equippable=equippable_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)
    # game_map.get_player(player)
    map_type = 'chunks'
    generate_map(game_map, player, map_type)
    # player.fov.calc_fov(game_map)
    game_map.get_player(player)
    game_state = GameStates.PLAYERS_TURN
    camera = Camera(constants['camera_width'], constants['camera_height'])
    camera.move_camera(player.x, player.y, game_map)
    message_log = MessageLog()

    return game_map, player, game_state, camera, message_log, map_type
