import itertools
from random import randint

from entity import Entity
from map_objects.chunks.make_bsp import make_bsp
from map_objects.chunks.noise_map import make_noise_map
from place_entities import place_entities


def generate_chunk(x, y, game_map):
    size = game_map.chunk_size

    assert x % size == 0
    assert y % size == 0

    if (x, y) in game_map.chunks:
        return

    game_map.chunks.add((x, y))
    chance = randint(0, 100)
    if chance > 90:
        print("bsp made", x, y)
        make_bsp(game_map, x, y, 6, 7)
    else:
        height_map, max_noise, min_noise = make_noise_map(x, y, size)

        for (j, k) in height_map:
            height_map[(j, k)] = (height_map[(j, k)] - min_noise)/(
                max_noise - min_noise)

            if height_map[(j, k)] < 0.3:
                # game_map.water[(j, k)] = Entity(j, k, '[U+504A]', 'white',
                # 'water')
                game_map.water[(j, k)] = Entity(j, k, '~', 'Water', 'blue',
                                                game_map.water)
            elif height_map[(j, k)] < 0.7:
                pass
            elif height_map[(j, k)] < 1:
                # walls = ['[U+2140]', '[U+2141]', '[U+2142]']
                # walls = ['[U+2140]', '[U+2141]', '[U+2142]']
                # r = randint(0, 2)
                # game_map.terrain[(j, k)] = Entity(j, k, walls[r], 'white',
                # 'wall')
                game_map.terrain[(j, k)] = Entity(j, k, '*', 'Mount', 'grey',
                                                  game_map.terrain)

    place_entities(x, y,
                   game_map,
                   game_map.chunk_size, game_map.chunk_size,
                   max_monsters_per_area=10,
                   max_items_per_area=6)


def add_new_chunks(game_map, player):
    cx = (player.x // game_map.chunk_size) * game_map.chunk_size
    cy = (player.y // game_map.chunk_size) * game_map.chunk_size
    chunk_size = game_map.chunk_size
    for x, y in itertools.product([cx - chunk_size, cx, cx + chunk_size],
                                  [cy - chunk_size, cy, cy + chunk_size]):
        generate_chunk(x, y, game_map)
