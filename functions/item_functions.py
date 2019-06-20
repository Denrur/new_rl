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