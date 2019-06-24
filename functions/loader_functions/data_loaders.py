import os

import shelve


def save_game(player, game_map, message_log, game_state, camera, map_type):
    with shelve.open('savegame.dat', 'n') as data_file:
        data_file['player_id'] = player.id
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state
        data_file['camera'] = camera
        data_file['map_type'] = map_type


def load_game():
    if not os.path.isfile('savegame.dat.dat'):
        raise FileNotFoundError

    with shelve.open('savegame.dat', 'r') as data_file:
        player_id = data_file['player_id']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']
        camera = data_file['camera']
        map_type = data_file['map_type']
        for entity in game_map.entities.values():
            if entity.id == player_id:
                player = entity

    return player, game_map, message_log, game_state, camera, map_type
