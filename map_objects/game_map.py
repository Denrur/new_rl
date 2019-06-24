from random import randint


class GameMap:
    def __init__(self, width, height, chunk_size=50, level=1):
        self.width = width
        self.height = height
        self.player = None
        self.full_rooms = True
        self.chunks = set()
        self.chunk_size = chunk_size
        self.entities = dict()
        self.terrain = dict()
        self.water = dict()
        self.objects = dict()
        self.items = dict()
        self.corpses = dict()
        self.stairs = dict()
        self.level = level

    def get_player(self, player):
        x = randint(0, self.width)
        y = randint(0, self.height)
        if (x, y) not in self.terrain:
            del self.entities[(player.x, player.y)]
            player.x, player.y = x, y
            self.entities[(x, y)] = player
            self.player = player
            player.fov.calc_fov(self)
        else:
            self.get_player(player)

    def is_unobstruct(self, x, y):
        if (x, y) in self.terrain:
            return False
        else:
            return True
