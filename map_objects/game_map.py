from entity import Entity


class GameMap:
    def __init__(self, width, height, chunk_size=50):
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

    def get_player(self, player):
        self.player = player

    def is_unobstruct(self, x, y):
        if (x, y) in self.terrain:
            return False
        else:
            return True

    # def initialize_terrain(self):
    #     for x in range(self.width):
    #         for y in range(self.height):
    #             Entity(x, y, '#', 'white', self.terrain)

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                del self.terrain[(x, y)]
