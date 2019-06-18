from bearlibterminal import terminal as blt
from camera import Camera
from components.fighter import Fighter
from entity import Entity
from components.fov import Fov
from game_states import GameStates
from input_handlers import handle_keys
# from map_objects.bsp.bsp_generator import make_bsp
from loader_functions.initialize_new_game import get_constants
from map_objects.chunks.chunk_generator import add_new_chunks
from map_objects.game_map import GameMap
from map_objects.map_generator import generate_map
from physics import movement
from render_functions import render_all


def main():
    constants = get_constants()
    screen_width = constants['screen_width']
    screen_height = constants['screen_height']
    map_width = constants['map_width']
    map_height = constants['map_height']
    camera_width = constants['camera_width']
    camera_height = constants['camera_height']
    game_map = GameMap(map_width, map_height)

    fov_component = Fov(game_map)
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(int(screen_width / 2),
                    int(screen_height / 2),
                    '@', 'You', 'white', game_map.entities,
                    fighter=fighter_component,
                    fov=fov_component)
    game_map.get_player(player)
    map_type = 'chunks'
    generate_map(game_map, player, map_type)

    camera = Camera(camera_width, camera_height)
    player.fov.calc_fov(game_map)
    render_all(game_map, player, camera)
    blt.refresh()
    game_state = GameStates.PLAYERS_TURN
    while True:
        blt.clear()

        # key = None
        # if blt.has_input():
        key = blt.read()

        action = handle_keys(game_state, key)

        move = action.get('move')
        fullscreen = action.get('fullscreen')
        exit = action.get('exit')

        if move and game_state == GameStates.PLAYERS_TURN:
            movement(move, game_map, player)
            player.fov.calc_fov(game_map)
            game_state = GameStates.ENEMY_TURN
            if map_type == 'chunks':
                add_new_chunks(game_map, player)

        if game_state == GameStates.ENEMY_TURN:
            completed_entities = []
            for entity in game_map.entities.values():
                if entity.ai:
                    if entity not in completed_entities:
                        entity.ai.take_turn(player, game_map)
                        completed_entities.append(entity)


            game_state = GameStates.PLAYERS_TURN
            # print(game_state)
        if fullscreen:
            blt.set("window: fullscreen=true;")
        if exit:
            return False

        render_all(game_map, player, camera)
        blt.refresh()


if __name__ == '__main__':
    blt.open()
    main()
    blt.close()