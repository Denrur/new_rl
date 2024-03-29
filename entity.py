import math
import uuid
from components.item import Item


class Entity:
    def __init__(self, x, y, char, name, color,
                 layer=None,
                 fighter=None, ai=None, fov=None,
                 item=None, inventory=None,
                 blocked=True,
                 block_sight=None,
                 stairs=None,
                 equipment=None,
                 equippable=None):
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocked = blocked
        self.layer = layer
        self.layer[(self.x, self.y)] = self
        self.explored = False
        self.fov = fov
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.equipment = equipment
        self.equippable = equippable

        if self.inventory:
            self.inventory.owner = self

        if self.item:
            self.item.owner = self

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.fov:
            self.fov.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

    def move(self, dx, dy):

        entity = self.layer.pop((self.x, self.y))
        self.x += dx
        self.y += dy
        self.layer[(self.x, self.y)] = entity

    def move_towards(self, target, game_map):
        dx = target.x - self.x
        dy = target.y - self.y
        distance = self.distance_to(target)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        x = self.x + dx
        y = self.y + dy
        if (((x, y) not in game_map.entities) and
                ((x, y) not in game_map.terrain)):
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


class Stairs:
    def __init__(self, floor):
        self.floor = floor
