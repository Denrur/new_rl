from map_objects.bsp.rectangle import Rect
from random import choice
from entity import Entity
# from components.fighter import Fighter
import functools
import tcod
from place_entities import place_entities


def make_bsp(game_map, depth, min_size, player,
             max_monsters_per_room, max_items_per_room):
    initialize_terrain(game_map)

    global rooms
    rooms = []
    full_rooms = False
    bsp = tcod.bsp_new_with_size(0, 0,
                                 game_map.width,
                                 game_map.height)

    tcod.bsp_split_recursive(bsp, 0, depth, min_size + 1, min_size + 1,
                             1.5, 1.5)

    tcod.bsp_traverse_inverted_level_order(bsp,
                                           functools.partial(
                                                traverse_node,
                                                full_rooms=full_rooms,
                                                game_map=game_map,
                                                entities=game_map.entities,
                                                mmpr=max_monsters_per_room,
                                                mipr=max_items_per_room,
                                                min_size=min_size,))

    player_room = choice(rooms)
    rooms.remove(player_room)
    player_room_x, player_room_y = player_room.center()
    game_map.entities.pop((player.x, player.y))
    player.x = player_room_x
    player.y = player_room_y
    game_map.entities[(player.x, player.y)] = player

    return game_map


def initialize_terrain(game_map):
    for x in range(game_map.width):
        for y in range(game_map.height):
            Entity(x, y, '#', 'white', game_map.terrain)


def traverse_node(node, _, game_map, entities, mmpr, mipr, min_size,
                  full_rooms):

    if tcod.bsp_is_leaf(node):
        minx = node.x + 1
        maxx = node.x + node.w - 1
        miny = node.y + 1
        maxy = node.y + node.h - 1
        if maxx == game_map.width - 1:
            maxx -= 1
        if maxy == game_map.height - 1:
            maxy -= 1
        if full_rooms is False:
            minx = tcod.random_get_int(None, minx,
                                       maxx - min_size + 1)
            miny = tcod.random_get_int(None, miny,
                                       maxy - min_size + 1)
            maxx = tcod.random_get_int(None, minx + min_size - 2,
                                       maxx)
            maxy = tcod.random_get_int(None, miny + min_size - 2,
                                       maxy)

        node.x = minx
        node.y = miny
        node.w = maxx - minx + 1
        node.h = maxy - miny + 1
        new_room = Rect(node.x, node.y, node.w, node.h)

        for x in range(minx, maxx + 1):
            for y in range(miny, maxy + 1):
                del game_map.terrain[(x, y)]
        place_entities(node.x, node.y, game_map, node.w, node.h, mmpr, mipr)

        rooms.append(new_room)

    else:
        left = tcod.bsp_left(node)
        right = tcod.bsp_right(node)
        node.x = min(left.x, right.x)
        node.y = min(left.y, right.y)
        node.w = max(left.x + left.w, right.x + right.w) - node.x
        node.h = max(left.y + left.h, right.y + right.h) - node.y

        if node.horizontal:
            if (left.x + left.w - 1 < right.x or
                    right.x + right.w - 1 < left.x):
                x1 = tcod.random_get_int(None, left.x,
                                         left.x + left.w - 1)
                x2 = tcod.random_get_int(None,
                                         right.x,
                                         right.x + right.w - 1)
                y = tcod.random_get_int(None, left.y + left.h, right.y)
                vline_up(game_map, x1, y - 1)
                hline(game_map, x1, y, x2)
                vline_down(game_map, x2, y + 1)
            else:
                minx = max(left.x, right.x)
                maxx = min(left.x + left.w - 1, right.x + right.w - 1)
                x = tcod.random_get_int(None, minx, maxx)

                while x > game_map.width - 1:
                    x -= 1
                vline_down(game_map, x, right.y)
                vline_up(game_map, x, right.y - 1)

        else:
            if (left.y + left.h - 1 < right.y or
                    right.y + right.h - 1 < left.y):
                y1 = tcod.random_get_int(None, left.y,
                                         left.y + left.h - 1)
                y2 = tcod.random_get_int(None, right.y,
                                         right.y + right.h - 1)
                x = tcod.random_get_int(None, left.x + left.w, right.x)
                hline_left(game_map, x - 1, y1)
                vline(game_map, x, y1, y2)
                hline_right(game_map, x + 1, y2)
            else:
                miny = max(left.y, right.y)
                maxy = min(left.y + left.h - 1, right.y + right.h - 1)
                y = tcod.random_get_int(None, miny, maxy)

                while y > game_map.height - 1:
                    y -= 1

                hline_left(game_map, right.x - 1, y)
                hline_right(game_map, right.x, y)

    return True


def vline(game_map, x, y1, y2):
    if y1 > y2:
        y1, y2 = y2, y1

    for y in range(y1, y2 + 1):
        del game_map.terrain[(x, y)]


def vline_up(game_map, x, y):
    while y >= 0 and (x, y) in game_map.terrain:
        del game_map.terrain[(x, y)]
        y -= 1


def vline_down(game_map, x, y):
    while y < game_map.height and (x, y) in game_map.terrain:
        del game_map.terrain[(x, y)]
        y += 1


def hline(game_map, x1, y, x2):
    if x1 > x2:
        x1, x2 = x2, x1
    for x in range(x1, x2 + 1):
        del game_map.terrain[(x, y)]


def hline_left(game_map, x, y):
    while x >= 0 and (x, y) in game_map.terrain:
        del game_map.terrain[(x, y)]
        x -= 1


def hline_right(game_map, x, y):
    while x < game_map.width and (x, y) in game_map.terrain:
        del game_map.terrain[(x, y)]
        x += 1
