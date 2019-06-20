from game_states import GameStates


def kill_entity(entity, game_map):
    entity.char = '%'
    entity.color = 'red'
    game_map.entities.pop((entity.x, entity.y))
    game_map.corpses[(entity.x, entity.y)] = entity
    if entity.name == 'You':
        return {'message': "You died", 'game_state': GameStates.PLAYER_DEAD}
    else:
        death_message = f'{entity.name} is dead'
        entity.fighter = None
        entity.ai = None
        entity.name = f'remains of {entity.name}'

        return {'message': death_message}
