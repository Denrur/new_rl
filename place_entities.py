from random import randint

from components.ai import BasicMonster
from components.fighter import Fighter
from components.fov import Fov
from components.item import Item
from entity import Entity
from functions.item_functions import heal


def place_entities(x, y,
                   game_map,
                   area_width,
                   area_height,
                   max_monsters_per_area,
                   max_items_per_area):
    number_of_monsters = randint(0, max_monsters_per_area)
    number_of_items = randint(0, max_items_per_area)

    for i in range(number_of_monsters):
        mx = randint(x + 1, x + area_width - 1)
        my = randint(y + 1, y + area_height - 1)

        if ((mx, my) not in game_map.entities or
                (mx, my) not in game_map.terrain):
            if randint(0, 100) < 80:
                fighter_component = Fighter(hp=10, defense=0, power=3)
                ai_component = BasicMonster()
                fov_component = Fov(game_map, radius=7)
                Entity(mx, my, 'z', 'Zombie', 'green',
                       game_map.entities,
                       fighter=fighter_component,
                       ai=ai_component,
                       fov=fov_component)
            else:
                fighter_component = Fighter(hp=16, defense=1, power=4)
                ai_component = BasicMonster()
                fov_component = Fov(game_map, radius=9)
                Entity(mx, my, 'r', 'Robot', 'red',
                       game_map.entities,
                       fighter=fighter_component,
                       ai=ai_component,
                       fov=fov_component)

    for i in range(number_of_items):
        mx = randint(x + 1, x + area_width - 1)
        my = randint(y + 1, y + area_height - 1)

        if ((mx, my) not in game_map.entities and
                (mx, my) not in game_map.terrain and
                (mx, my) not in game_map.items):
            if randint(0, 100) < 80:
                item_component = Item(use_function=heal, amount=4)
                Entity(mx, my, '!', 'Healing potion', 'violet',
                       game_map.items,
                       item=item_component)

            else:
                item_component = Item()
                Entity(mx, my, '#', 'Scroll', 'red',
                       game_map.items,
                       item=item_component)