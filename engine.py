from time import time

from bearlibterminal import terminal as blt

from camera import Camera
from components.fighter import Fighter
from components.fov import Fov
from components.inventory import Inventory
from entity import Entity
from functions.loader_functions.initialize_new_game import get_constants
from UI.game_messages import MessageLog
from game_states import GameStates
from input_handlers import handle_keys
from map_objects.chunks.chunk_generator import add_new_chunks
from map_objects.game_map import GameMap
from map_objects.map_generator import generate_map
from physics import movement
from render_functions import render_all
from result_listner import show_result
from UI.frame import FrameWithScrollbar


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
    fighter_component = Fighter(hp=3000, defense=2, power=5)
    inventory_component = Inventory(26)
    player = Entity(int(screen_width / 2),
                    int(screen_height / 2),
                    '@', 'You', 'white', game_map.entities,
                    fighter=fighter_component,
                    fov=fov_component,
                    inventory=inventory_component)

    game_map.get_player(player)
    map_type = 'chunks'
    generate_map(game_map, player, map_type)

    camera = Camera(camera_width, camera_height)
    message_log = MessageLog()
    log_frame = FrameWithScrollbar(message_log, 'dark orange')
    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state
    player.fov.calc_fov(game_map)
    render_all(game_map, player, camera, game_state, log_frame)
    blt.refresh()
    targeting_item = None
    while True:
        # mouse_x = blt.state(blt.TK_MOUSE_X)
        # mouse_y = blt.state(blt.TK_MOUSE_Y)
        # mouse = (mouse_x, mouse_y)
        # player.fov.calc_fov(game_map)
        # render_all(game_map, player, camera)
        blt.clear()
        # message_log = MessageLog()
        # key = None
        # if blt.has_input():
        key = blt.read()
        action = handle_keys(game_state, key)
        # mouse_action = handle_mouse(mouse)
        move = action.get('move')
        fullscreen = action.get('fullscreen')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        left_click = action.get('left_click')
        right_click = action.get('right_click')
        exit = action.get('exit')

        start_loop = time()
        player_turn_results = list()

        if move and game_state == GameStates.PLAYERS_TURN:
            player_turn_result = movement(move, game_map, player)
            player_turn_results.extend(player_turn_result)
            player.fov.calc_fov(game_map)
            game_state = GameStates.ENEMY_TURN
            if map_type == 'chunks':
                add_new_chunks(game_map, player)

        if pickup and game_state == GameStates.PLAYERS_TURN:
            if (player.x, player.y) in game_map.items:
                item = game_map.items[(player.x, player.y)]

                pickup_results = player.inventory.add_item(item)
                player_turn_results.extend(pickup_results)

            else:
                message_log.append('There is nothing here to pick up')

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if (inventory_index is not None and
                previous_game_state != GameStates.PLAYER_DEAD
                and inventory_index < len(player.inventory.items)):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=game_map.entities,))
                # fov=player.fov.fov_cells))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))
        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = camera.to_map_coordinates(left_click[0],
                                                               left_click[1])

                item_use_results = player.inventory.use(player.inventory.targeting_item,
                                                        entities=game_map.entities,
                                                        target_x=target_x,
                                                        target_y=target_y)
                player_turn_results.extend(item_use_results)

            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})



        if player_turn_results:
            state = show_result(player_turn_results,
                                game_state,
                                game_map,
                                message_log,
                                player)
            if state:
                game_state = state

        if fullscreen:
            blt.set("window: fullscreen=true;")
        if exit:
            if game_state in (GameStates.SHOW_INVENTORY,
                              GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                return False

        if game_state == GameStates.ENEMY_TURN:
            completed_entities = []
            entities = [game_map.entities.get((x, y)) for (x, y) in set(player.fov.fov_cells) & set(game_map.entities)]
            # for x, y in player.fov.fov_cells:
            for entity in entities:
                # if (x, y) in game_map.entities:
                # entity = game_map.entities.get((x, y))
                if entity is not None and entity.ai:
                    if entity not in completed_entities:
                        enemy_turn_results = entity.ai.take_turn(player,
                                                                 game_map)
                        completed_entities.append(entity)
                        state = show_result(enemy_turn_results,
                                            game_state,
                                            game_map, message_log,
                                            entity)
                        if state:
                            game_state = state
                        if game_state == GameStates.PLAYER_DEAD:
                            break
                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN
            # print(i)
        render_all(game_map, player, camera, game_state, log_frame, action,
                   debug=True)
        end_loop = time()
        print(end_loop - start_loop)
        # blt.refresh()


if __name__ == '__main__':
    blt.open()
    main()
    blt.close()
