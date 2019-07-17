from bearlibterminal import terminal as blt

from actions import entity_action
from UI.frame import FrameWithScrollbar
from UI.ui import main_menu, message_box
from functions.loader_functions.data_loaders import load_game
from functions.loader_functions.initialize_new_game import get_constants, get_game_variables
from game_states import EntityStates, GameStates
from functions.input_handlers import handle_main_menu
from functions.render_functions import render_all


def main():
    constants = get_constants()

    game_map = None

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
                game_map = (get_game_variables(constants))
                # game_map.get_player(player)

                show_main_menu = False
            elif load_saved_game:
                try:
                    game_map = load_game()

                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            blt.clear()
            play_game(game_map)

            show_main_menu = True


def play_game(game_map):

    player = game_map.player
    log_frame = FrameWithScrollbar(game_map.message_log, 'dark orange')
    render_all(game_map, log_frame)
    # fps = 25
    blt.refresh()

    q = game_map.time_schedule
    game_map.game_state = GameStates.SESSION

    while game_map.game_state != GameStates.MENU:

        entities = [game_map.entities.get((x, y)) for (x, y) in set(player.fov.fov_cells) & set(game_map.entities)]

        for entity in entities:
            if entity not in q.scheduled_events.queue:
                q.schedule_event(entity, entity.action_delay)

        entity = q.next_event()
        entity_action(entity, game_map, log_frame, q)
        print(game_map.game_state)
        blt.clear()

        # if entity.state != EntityStates.DEAD:
        #     q.schedule_event(entity, entity.action_delay)


if __name__ == '__main__':
    blt.open()
    main()
    blt.close()
