from map_objects.chunks.make_bsp import make_bsp
from map_objects.chunks.chunk_generator import add_new_chunks


def generate_map(game_map, player, map_type):
    print(game_map.terrain)
    if map_type == 'bsp':
        make_bsp(game_map, 0, 0, 6, 7)
    elif map_type == 'chunks':
        add_new_chunks(game_map, player)
