from components import rpas


class Fov:
    def __init__(self, game_map, radius=10):
        self.radius = radius
        self.game_map = game_map

    def calc_fov(self, game_map):
        self.fov_cells = set()
        x = self.owner.x
        y = self.owner.y
        fov = rpas.FOVCalc()
        is_unobstruct = game_map.is_unobstruct
        self.fov_cells = fov.calc_visible_cells_from(x, y, self.radius,
                                                     is_unobstruct)
