from functions.death_functions import kill_entity
from game_states import GameStates


def show_result(results, game_state, game_map, message_log, entity):
    if results:
        for result in results:
            message = result.get('message')
            dead_entity = result.get('dead')
            item_added = result.get('item_added')
            item_consumed = result.get('consumed')
            item_dropped = result.get('item_dropped')
            targeting = result.get('targeting')
            targeting_cancelled = result.get('targeting_cancelled')
            if message:
                message_log.append(message)

            if dead_entity:
                if dead_entity.name == 'You':
                    result = kill_entity(dead_entity, game_map)
                    game_state = result.get('game_state', game_state)
                else:
                    result = kill_entity(dead_entity, game_map)
                    game_state = result.get('game_state', game_state)

            if item_added:
                del item_added.layer[(item_added.x, item_added.y)]
                # del game_map.items[(item_added.x, item_added.y)]

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN
                # message = result.get('message')
                # message_log.append(message)
            if targeting:
                game_state = GameStates.TARGETING
                entity.inventory.targeting_item = targeting_item = targeting
                message_log.append(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = GameStates.SHOW_INVENTORY
                message_log.append('Targeting cancelled')

            if item_dropped:
                item_dropped.layer[(entity.x, entity.y)] = item_dropped
                game_state = GameStates.ENEMY_TURN

        return game_state
