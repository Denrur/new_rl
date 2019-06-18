from map_objects.bsp.bsp_generator import make_bsp
from map_objects.chunks.chunk_generator import add_new_chunks


def generate_map(game_map, player, map_type):
    if map_type == 'bsp':
        make_bsp(game_map, 15, 10, player, 2, 3)
    elif map_type == 'chunks':
        add_new_chunks(game_map, player)
