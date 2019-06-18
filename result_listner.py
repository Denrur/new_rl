from death_functions import kill_entity


def show_result(results, game_state, game_map):
    if results:
        for result in results:
            message = result.get('message')
            dead_entity = result.get('dead')

            if message:
                print(message)

            if dead_entity:
                if dead_entity.name == 'You':
                    result = kill_entity(dead_entity, game_map)
                    message = result.get('message')
                    game_state = result.get('game_state', game_state)
                else:
                    result = kill_entity(dead_entity, game_map)
                    message = result.get('message')
                    game_state = result.get('game_state', game_state)
                print(message)

                return game_state
