from game_states import GameStates, EntityStates


def kill_entity(entity, game_map):
    entity.char = '%'
    entity.color = 'red'
    print((entity.x, entity.y))
    entity.change_layer(game_map.corpses)
    entity.state = EntityStates.DEAD
    if entity.name == 'You':
        return {'message': "You died", 'game_state': entity.state}
    else:
        death_message = f'{entity.name} is dead'
        entity.fighter = None
        entity.ai = None
        entity.name = f'remains of {entity.name}'

        return {'message': death_message}
