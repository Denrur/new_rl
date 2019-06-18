from bearlibterminal import terminal as blt
from pathfinding.graph import GridWithWeights
from pathfinding.dijkstra import dijkstra_search, reconstruct_path
from pathfinding.a_star_search import a_star_search
from physics import movement

class BasicMonster:
    def take_turn(self, target, game_map):
        monster = self.owner
        monster.fov.calc_fov(game_map)
        if (target.x, target.y) in monster.fov.fov_cells:
            # if monster.distance_to(target) >= 2:
            start = (monster.x, monster.y)
            goal = (target.x, target.y)
            graph = GridWithWeights(game_map, monster.x, monster.y, 10)
            came_from, cost_so_far = dijkstra_search(graph, start, goal)
            # came_from, cost_so_far = a_star_search(graph, start, goal)
            path = reconstruct_path(came_from, start, goal)

            coords = path.pop(0)
            destination = (coords[0] - monster.x, coords[1] - monster.y)

            movement(destination, game_map, monster)

            # print(f'{monster.name} moves towards {target.name}')


            # print(f'The {self.owner.name} wonders when it will get to move')
