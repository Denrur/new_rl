from functions.death_functions import kill_entity
from game_states import EntityStates


def show_result(results, game_map, entity):
    if results:
        for result in results:
            message = result.get('message')
            dead_entity = result.get('dead')
            item_added = result.get('item_added')
            item_consumed = result.get('consumed')
            item_dropped = result.get('item_dropped')
            equip = result.get('equip')
            targeting = result.get('targeting')
            targeting_cancelled = result.get('targeting_cancelled')
            if message:
                game_map.message_log.append(message)

            if dead_entity:
                if dead_entity.name == 'You':
                    kill_entity(dead_entity, game_map)
                else:
                    kill_entity(dead_entity, game_map)

            if item_added:
                del item_added.layer[(item_added.x, item_added.y)]
                entity.state = EntityStates.PASS_TURN

            if item_consumed:
                entity.state = EntityStates.PASS_TURN

            if targeting:
                entity.state = EntityStates.TARGETING
                entity.inventory.targeting_item = targeting_item = targeting
                game_map.message_log.append(targeting_item.item.targeting_message)

            if targeting_cancelled:
                entity.state = EntityStates.SHOW_INVENTORY
                game_map.message_log.append('Targeting cancelled')

            if item_dropped:
                item_dropped.layer[(entity.x, entity.y)] = item_dropped
                entity.state = EntityStates.PASS_TURN

            if equip:
                equip_results = entity.equipment.toggle_equip(equip)

                for equip_result in equip_results:
                    equiped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equiped:
                        game_map.message_log.append(f'You equipped the {equiped.name}')

                    if dequipped:
                        game_map.message_log.append(f'You dequipped the {dequipped.name}')
                entity.state = EntityStates.PASS_TURN
