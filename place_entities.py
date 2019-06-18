from components.fighter import Fighter
from components.ai import BasicMonster
from entity import Entity
from components.fov import Fov
from random import randint


def place_entities(x, y,
                   game_map,
                   area_width,
                   area_height,
                   max_monsters_per_area,
                   max_items_per_area):
    number_of_monsters = randint(0, max_monsters_per_area)

    for i in range(number_of_monsters):
        mx = randint(x + 1, x + area_width - 1)
        my = randint(y + 1, y + area_height - 1)

        if ((mx, my) not in game_map.entities or
                (mx, my) not in game_map.terrain):
            if randint(0, 100) < 80:
                fighter_component = Fighter(hp=10, defense=0, power=3)
                ai_component = BasicMonster()
                fov_component = Fov(game_map, radius=7)
                monster = Entity(mx, my, 'z', 'Zombie', 'green',
                                 game_map.entities,
                                 fighter=fighter_component,
                                 ai=ai_component,
                                 fov=fov_component)
            else:
                fighter_component = Fighter(hp=16, defense=1, power=4)
                ai_component = BasicMonster()
                fov_component = Fov(game_map, radius=9)
                monster = Entity(mx, my, 'r', 'Robot', 'red',
                                 game_map.entities,
                                 fighter=fighter_component,
                                 ai=ai_component,
                                 fov=fov_component)

            game_map.entities[(mx, my)] = monster
