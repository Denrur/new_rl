import os

import shelve


def save_game(game_map):
    with shelve.open('savegame.dat', 'n') as data_file:
        data_file['player_id'] = game_map.player.id
        data_file['game_map'] = game_map


def load_game():
    if not os.path.isfile('savegame.dat.db'):
        raise FileNotFoundError

    with shelve.open('savegame.dat', 'r') as data_file:
        # player_id = data_file['player_id']
        game_map = data_file['game_map']

        # for entity in game_map.entities.values():
        #     if entity.id == player_id:
        #         player = entity

    return game_map
