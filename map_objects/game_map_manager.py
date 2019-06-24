class GameMapManager:
    def __init__(self):
        self.game_maps = dict()

    def add_game_map(self, game_map):
        self.game_maps[game_map.level] = game_map

    def remove_game_map(self, game_map):
        del self.game_maps[game_map.level]
