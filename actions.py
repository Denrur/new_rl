from game_states import EntityStates, GameStates
from result_listner import show_result
from functions.render_functions import render_all


def entity_action(entity, game_map, log_frame, q):
    entity.state = EntityStates.IDLE
    print('Entity state', entity.name, entity.state)

    if entity is not None and entity.ai:
        while entity.state != EntityStates.PASS_TURN and game_map.game_state == GameStates.SESSION:
            entity.action_cost = 100
            entity_turn_results = entity.ai.take_turn(game_map, game_map.player)
            print(game_map.game_state)
            show_result(entity_turn_results, game_map, entity)
            render_all(game_map, log_frame, debug=True)
        if entity.state != EntityStates.DEAD:
            q.schedule_event(entity, entity.action_delay)
