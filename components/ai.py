from random import randint
from bearlibterminal import terminal as blt
from functions.input_handlers import handle_keys
from pathfinding.a_star_search import a_star_search
from pathfinding.dijkstra import reconstruct_path
from pathfinding.graph import GridWithWeights
from physics import movement
from game_states import EntityStates, GameStates
from functions.loader_functions.data_loaders import save_game


class Player:
    def take_turn(self, game_map, target=None):
        from map_objects.chunks.chunk_generator import add_new_chunks
        entity = self.owner
        # while entity.state != EntityStates.PASS_TURN:
        key = blt.read()
        action = handle_keys(entity, key)
        move = action.get('move')
        fullscreen = action.get('fullscreen')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        left_click = action.get('left_click')
        right_click = action.get('right_click')
        exit_game = action.get('exit')

        results = list()

        if move and entity.state == EntityStates.IDLE:
            player_turn_result = movement(move, game_map, entity)
            results.extend(player_turn_result)
            entity.fov.calc_fov(game_map)
            entity.action_cost = 100
            if game_map.map_type == 'chunks':
                add_new_chunks(game_map, entity)
            entity.state = EntityStates.PASS_TURN

        if pickup and entity.state == EntityStates.IDLE:
            if (entity.x, entity.y) in game_map.items:
                item = game_map.items[(entity.x, entity.y)]

                pickup_results = entity.inventory.add_item(item)
                results.extend(pickup_results)

            else:
                game_map.message_log.append('There is nothing here to pick up')

        if show_inventory and entity.state == EntityStates.IDLE:
            entity.state = EntityStates.SHOW_INVENTORY

        if drop_inventory and entity.state == EntityStates.IDLE:
            entity.state = EntityStates.DROP_INVENTORY

        if inventory_index is not None and inventory_index < len(entity.inventory.items):
            item = entity.inventory.items[inventory_index]

            if entity.state == EntityStates.SHOW_INVENTORY:
                results.extend(entity.inventory.use(item, entities=game_map.entities))

            elif entity.state == EntityStates.DROP_INVENTORY:
                results.extend(entity.inventory.drop_item(item))

        if entity.state == EntityStates.TARGETING:
            if left_click:
                target_x, target_y = game_map.camera.to_map_coordinates(left_click[0], left_click[1])

                item_use_results = entity.inventory.use(entity.inventory.targeting_item,
                                                        entities=game_map.entities,
                                                        target_x=target_x,
                                                        target_y=target_y)
                results.extend(item_use_results)
                entity.state = EntityStates.PASS_TURN

            elif right_click:
                results.append({'targeting_cancelled': True})
                entity.state = EntityStates.SHOW_INVENTORY

        # if results:
        #     print(self.owner.name, results)
        #     return results, GameStates.SESSION

        if fullscreen:
            blt.set("window: fullscreen=true;")

        if exit_game:
            if entity.state in (EntityStates.SHOW_INVENTORY,
                                EntityStates.DROP_INVENTORY):
                entity.state = EntityStates.IDLE
            elif entity.state == EntityStates.TARGETING:
                results.append({'targeting_cancelled': True})
            else:
                save_game(game_map)
                print("Game saved")
                game_map.game_state = GameStates.MENU
                return results

        return results


class BasicMonster:
    def take_turn(self, game_map, target=None):
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

        monster.state = EntityStates.PASS_TURN
        print(self.owner.name, results)
        return results


class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.owner = None
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, game_map, target=None):
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
        monster.state = EntityStates.PASS_TURN
        print(self.owner.name, results)
        return results
