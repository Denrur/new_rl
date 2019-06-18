def movement(destination, game_map, entity):
    # print(type(type(destination)))
    if isinstance(destination, tuple):
        dx, dy = destination
        dest_x = entity.x + dx
        dest_y = entity.y + dy
    else:
        dx, dy = destination.x - entity.x, destination.y - entity.y
        print('dx, dy', dx, dy)
        distance = entity.distance_to(destination)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        dest_x = entity.x + dx
        dest_y = entity.y + dy
    if (dest_x, dest_y) in game_map.terrain:
        return
    if game_map.entities.get((dest_x, dest_y)):
        target = game_map.entities.get((dest_x, dest_y))
        if target.fighter.hp > 0 and entity.name != target.name:
            print(f'{entity.name} kick the {target.name}')
    else:
        # print(entity.name, entity.x, entity.y)
        entity.move(dx, dy)
        # print(entity.name, entity.x, entity.y)
