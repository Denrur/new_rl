from pathfinding.a_star_search import a_star_search
from pathfinding.dijkstra import reconstruct_path
from pathfinding.graph import GridWithWeights
from physics import movement


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
