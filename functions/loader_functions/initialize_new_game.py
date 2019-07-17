from bearlibterminal import terminal as blt

from UI.game_messages import MessageLog
from camera import Camera
from components.ai import Player
from components.equipment import Equipment, EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.fov import Fov
from components.inventory import Inventory
from entity import Entity
from map_objects.game_map import GameMap
from map_objects.map_generator import generate_map
from utilities.time_schedule import TimeSchedule


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
    camera = Camera(constants['camera_width'], constants['camera_height'])
    message_log = MessageLog()
    fighter_component = Fighter(hp=3000, defense=2, power=5)
    inventory_component = Inventory(26)
    time_schedule = TimeSchedule()
    game_map = GameMap(constants['map_width'], constants['map_height'],
                       time_schedule, camera, message_log)
    fov_component = Fov(game_map)
    equipment_component = Equipment()
    ai_component = Player()
    player = Entity(0, 0,
                    '@', 'You', 'white', layer=game_map.entities,
                    fighter=fighter_component,
                    fov=fov_component,
                    inventory=inventory_component,
                    equipment=equipment_component,
                    ai=ai_component)
    game_map.time_schedule.schedule_event(player, player.action_delay)

    equippable_component = Equippable(EquipmentSlots.RIGHT_HAND, power_bonus=2)
    dagger = Entity(0, 0, '-', 'Dagger', 'blue', game_map.items,
                    equippable=equippable_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)
    generate_map(game_map, player, game_map.map_type)
    game_map.get_player(player)
    camera = Camera(constants['camera_width'], constants['camera_height'])
    camera.move_camera(player.x, player.y, game_map)

    return game_map
