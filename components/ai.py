from pathfinding.a_star_search import a_star_search
from pathfinding.dijkstra import reconstruct_path
from pathfinding.graph import GridWithWeights
from physics import movement
from random import randint


class BasicMonster:
    def take_turn(self, target, game_map):
        results = list()
        monster = self.owner
        monster.fov.calc_fov(game_map)

        if (target.x, target.y) in monster.fov.fov_cells:
            start = (monster.x, monster.y)
            goal = (target.x, target.y)
            graph = GridWithWeights(game_map, monster.x, monster.y, 10)
            # came_from, cost_so_far = dijkstra_search(graph, start, goal)
            came_from, cost_so_far = a_star_search(graph, start, goal)
            path = reconstruct_path(came_from, start, goal)
            coords = path.pop(0)
            destination = (coords[0] - monster.x, coords[1] - monster.y)
            results.extend(movement(destination, game_map, monster))

        return results


class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.owner = None
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, game_map):
        results = list()
        monster = self.owner

        if self.number_of_turns > 0:
            random_x = randint(0, 2) - 1
            random_y = randint(0, 2) - 1
            destination = (random_x, random_y)
            if (random_x, random_y) != (0, 0):
                results.extend(movement(destination, game_map, monster))
            self.number_of_turns -= 1

        else:
            self.owner.ai = self.previous_ai
            results.append({'message': f'The {monster.name} is no longer confused'})

        return results
