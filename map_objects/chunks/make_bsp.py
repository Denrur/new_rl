import copy
import random

import tcod

from entity import Entity
from place_entities import place_entities


def make_bsp(game_map, cx, cy, depth, min_room_size):
    full_rooms = True
    bsp = tcod.bsp.BSP(cx, cy, game_map.chunk_size - 1,
                       game_map.chunk_size - 1)
    initialize_terrain(game_map, cx, cy)
    bsp_generate(bsp, game_map, depth, min_room_size, cx, cy, full_rooms)


def initialize_terrain(game_map, cx, cy):
    for x in range(cx, cx + game_map.chunk_size):
        for y in range(cy, cy + game_map.chunk_size):
            if x == cx or x == cx + game_map.chunk_size - 1:
                Entity(x, y, '=', 'Wall', 'grey', game_map.terrain)
            elif y == cy or y == cy + game_map.chunk_size - 1:
                Entity(x, y, '=', 'Wall', 'grey', game_map.terrain)
            else:
                Entity(x, y, '#', 'Wall', 'grey', game_map.terrain)


def bsp_generate(bsp, game_map, depth, min_room_size, cx, cy, full_rooms):
    bsp.children = ()
    bsp.split_recursive(depth,
                        min_room_size,
                        min_room_size,
                        1.5,
                        1.5)
    for node in copy.deepcopy(bsp).inverted_level_order():
        traverse_node(game_map, node, cx, cy, min_room_size,
                      full_rooms)


# the class building the dungeon from the bsp nodes
def traverse_node(game_map, node, cx, cy, min_size,
                  full_rooms):
    if not node.children:
        minx = node.x + 1
        maxx = node.x + node.w - 1
        miny = node.y + 1
        maxy = node.y + node.h - 1
        if maxx == game_map.chunk_size - 1:
            maxx -= 1
        if maxy == game_map.chunk_size - 1:
            maxy -= 1
        if full_rooms is False:
            minx = random.randint(minx, maxx - min_size + 1)
            miny = random.randint(miny, maxy - min_size + 1)
            maxx = random.randint(minx + min_size - 2, maxx)
            maxy = random.randint(miny + min_size - 2, maxy)

        node.x = minx
        node.y = miny
        node.w = maxx - minx + 1
        node.h = maxy - miny + 1

        for x in range(minx, maxx + 1):
            for y in range(miny, maxy + 1):
                del game_map.terrain[(x, y)]

        place_entities(node.x, node.y, game_map, node.w, node.h,
                       max_monsters_per_area=3, max_items_per_area=2)

    else:
        # resize the node to fit its sons
        left, right = node.children
        node.x = min(left.x, right.x)
        node.y = min(left.y, right.y)
        node.w = max(left.x + left.w, right.x + right.w) - node.x
        node.h = max(left.y + left.h, right.y + right.h) - node.y
        # create a corridor between the two lower nodes
        if node.horizontal:
            # vertical corridor
            if (left.x + left.w - 1 < right.x or
                    right.x + right.w - 1 < left.x):
                # no overlapping zone. we need a Z shaped corridor
                x1 = random.randint(left.x, left.x + left.w - 1)
                x2 = random.randint(right.x, right.x + right.w - 1)
                y = random.randint(left.y + left.h, right.y)
                vline_up(game_map, x1, y - 1, cy)
                hline(game_map, x1, y, x2)
                vline_down(game_map, x2, y + 1, cy)
            else:
                # straight vertical corridor
                minx = max(left.x, right.x)
                maxx = min(left.x + left.w - 1, right.x + right.w - 1)
                x = random.randint(minx, maxx)
                vline_down(game_map, x, right.y, cy)
                vline_up(game_map, x, right.y - 1, cy)
        else:
            # horizontal corridor
            if (left.y + left.h - 1 < right.y or
                    right.y + right.h - 1 < left.y):
                # no overlapping zone. we need a Z shaped corridor
                y1 = random.randint(left.y, left.y + left.h - 1)
                y2 = random.randint(right.y, right.y + right.h - 1)
                x = random.randint(left.x + left.w, right.x)
                hline_left(game_map, x - 1, y1, cx)
                vline(game_map, x, y1, y2)
                hline_right(game_map, x + 1, y2, cx)
            else:
                # straight horizontal corridor
                miny = max(left.y, right.y)
                maxy = min(left.y + left.h - 1, right.y + right.h - 1)
                y = random.randint(miny, maxy)
                hline_left(game_map, right.x - 1, y, cx)
                hline_right(game_map, right.x, y, cx)


# draw a vertical line
def vline(game_map, x, y1, y2):
    if y1 > y2:
        y1, y2 = y2, y1
    for y in range(y1, y2 + 1):
        del game_map.terrain[(x, y)]


# draw a vertical line up until we reach an empty space
def vline_up(game_map, x, y, cy):
    while y >= cy and (x, y) in game_map.terrain:
        del game_map.terrain[(x, y)]
        y -= 1


# draw a vertical line down until we reach an empty space
def vline_down(game_map, x, y, cy):
    while y < cy + game_map.chunk_size and (x, y) in game_map.terrain:
        del game_map.terrain[(x, y)]
        y += 1


# draw a horizontal line
def hline(game_map, x1, y, x2):
    if x1 > x2:
        x1, x2 = x2, x1
    for x in range(x1, x2 + 1):
        del game_map.terrain[(x, y)]


# draw a horizontal line left until we reach an empty space
def hline_left(game_map, x, y, cx):
    while x >= cx and (x, y) in game_map.terrain:
        del game_map.terrain[(x, y)]
        x -= 1


# draw a horizontal line right until we reach an empty space
def hline_right(game_map, x, y, cx):
    while x < cx + game_map.chunk_size and (x, y) in game_map.terrain:
        del game_map.terrain[(x, y)]
        x += 1
