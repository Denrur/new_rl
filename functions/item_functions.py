from components.ai import ConfusedMonster


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = list()

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({
            'consumed': False,
            'message' : f'{entity.name} have a full health'
            })
    else:
        entity.fighter.heal(amount)
        results.append({
            'consumed': True,
            'message' : f'{entity.name} feel better'
            })
    print(results)
    return results


def cast_lightning(*args, **kwargs):

    caster = args[0]
    print(caster.name)
    entities = kwargs.get('entities')
    fov_map = caster.fov.fov_cells
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = list()

    target = None
    closest_distance = maximum_range + 1
    # entities_in_fov = None
    # print(set(entities) & set(fov_map))

    entities_in_fov = list(set(entities.keys()) & set(fov_map))

    if entities_in_fov:
        for coords in entities_in_fov:
            entity = entities[coords]
            if entity.fighter and entity != caster:
                distance = caster.distance_to(entity)

                if distance < closest_distance:
                    target = entity
                    closest_distance = distance

    if target:
        results.append({'consumed': True,
                        'target': target,
                        'message':
                            f'''A bolt strikes the {target.name} with a loud thunder! The damage is {damage}'''})
        results.extend(target.fighter.take_damage(damage))

    else:
        results.append({'consumed': False, 'target': None, 'message': 'No enemy is close enough to strike'})

    return results


def cast_fireball(*args, **kwargs):
    caster = args[0]
    print(caster.name)
    entities = kwargs.get('entities')
    fov_map = caster.fov.fov_cells
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = list()

    # entities_in_fov = list(set(entities.keys()) & set(fov_map))
    print(fov_map)
    print(target_x, target_y)
    if (target_x, target_y) not in fov_map:
        results.append({'consumed': False, 'message': 'You cannot see the target'})
        return results

    results.append({'consumed': True, 'message': f'Fireball explodes, burning everything within {radius} tiles'})

    for x in range(target_x - radius, target_x + radius + 1):
        for y in range(target_y - radius, target_y + radius + 1):
            if (x, y) in entities:
                entity = entities[(x, y)]
                if (target_x, target_y) in entity.fov.fov_cells:
                    results.append({'message': f'The {entity.name} gets burned for {damage} hit points'})
                    results.extend(entity.fighter.take_damage(damage))

    return results


def cast_confuse(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = caster.fov.fov_cells
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if (target_x, target_y) not in fov_map:
        results.append({'consumed': False, 'message': 'You cannot target a tile outside your field of view.'})
        return results

    entity = entities.get((target_x, target_y))
    if entity.ai:
        confused_ai = ConfusedMonster(entity.ai, 10)

        confused_ai.owner = entity
        entity.ai = confused_ai

        results.append({'consumed': True,
                        'message': f'The eyes of the {entity.name} look vacant, as he starts to stumble around!'})

    else:
        results.append({'consumed': False,
                        'message': 'There is no targetable enemy at that location.'})

    return results
