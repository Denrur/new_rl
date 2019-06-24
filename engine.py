from time import time

from bearlibterminal import terminal as blt


from functions.loader_functions.initialize_new_game import get_constants, get_game_variables
from functions.loader_functions.data_loaders import load_game, save_game
from game_states import GameStates
from input_handlers import handle_keys, handle_main_menu
from map_objects.chunks.chunk_generator import add_new_chunks
from physics import movement
from render_functions import render_all
from result_listner import show_result
from UI.frame import FrameWithScrollbar
from UI.ui import main_menu, message_box


def main():
    constants = get_constants()

    player = None
    game_map = None
    message_log = None
    game_state = None
    camera = None
    map_type = None

    show_main_menu = True
    show_load_error_message = False

    while True:
        if show_main_menu:
            main_menu(constants['screen_width'], constants['screen_height'])

            if show_load_error_message:
                message_box('No save game to load', 50,
                            constants['screen_width'],
                            constants['screen_height'])
            blt.refresh()

            action = handle_main_menu()

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if (show_load_error_message and
                    (new_game or load_saved_game or exit_game)):
                show_load_error_message = False
            elif new_game:
                (game_map,
                 player,
                 game_state,
                 camera,
                 message_log,
                 map_type) = (get_game_variables(constants))
                game_map.get_player(player)

                show_main_menu = False
            elif load_saved_game:
                try:
                    (player, game_map, message_log, game_state, camera, map_type) = load_game()

                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            blt.clear()
            play_game(game_map, player, game_state, camera, message_log, map_type)

            show_main_menu = True


def play_game(game_map, player, game_state, camera, message_log, map_type):

    log_frame = FrameWithScrollbar(message_log, 'dark orange')

    previous_game_state = game_state

    render_all(game_map, player, camera, game_state, log_frame)
    blt.refresh()
    # targeting_item = None
    while True:

        blt.clear()

        key = blt.read()
        action = handle_keys(game_state, key)
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
                save_game(player, game_map, message_log, game_state, camera, map_type)

                return False

        if game_state == GameStates.ENEMY_TURN:
            completed_entities = []
            entities = [game_map.entities.get((x, y)) for (x, y) in set(player.fov.fov_cells) & set(game_map.entities)]
            for entity in entities:
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
        render_all(game_map, player, camera, game_state, log_frame, action,
                   debug=True)
        end_loop = time()
        print(end_loop - start_loop)


if __name__ == '__main__':
    blt.open()
    main()
    blt.close()
