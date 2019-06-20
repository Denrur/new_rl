from bearlibterminal import terminal as blt
from UI.ui import ui


def render_all(game_map, player, camera, log_frame, action=None, debug=False):
    entities = game_map.entities
    corpses = game_map.corpses
    terrain = game_map.terrain
    water = game_map.water
    camera.move_camera(player.x, player.y, game_map)

    for x in range(camera.width):
        for y in range(camera.height):

            map_x, map_y = camera.to_map_coordinates(x, y)
            if (map_x, map_y) in player.fov.fov_cells:

                if (map_x, map_y) in water:
                    render_obj((map_x, map_y), water, camera, 'blue')
                    water.get((map_x, map_y)).explored = True

                if (map_x, map_y) in terrain:
                    obj = terrain.get((map_x, map_y))
                    render_obj((map_x, map_y), terrain, camera, obj.color)
                    terrain.get((map_x, map_y)).explored = True

                if (map_x, map_y) in corpses:
                    obj = corpses.get((map_x, map_y))
                    render_obj((map_x, map_y), corpses, camera, obj.color)

                if (map_x, map_y) in entities:
                    obj = entities.get((map_x, map_y))
                    render_obj((map_x, map_y), entities, camera, obj.color)

            elif ((map_x, map_y) in terrain and
                    terrain.get((map_x, map_y)).explored):
                render_obj((map_x, map_y), terrain, camera, 'darker orange')

            elif ((map_x, map_y) in water and
                    water.get((map_x, map_y)).explored):
                render_obj((map_x, map_y), water, camera, 'darker blue')

    ui(player, camera, log_frame, action)
    # print('Map layer', blt.state(blt.TK_LAYER))
    # render_bar(1, camera.height + 1, 10, 'HP', player.fighter.hp, player.fighter.max_hp,
    #            'dark red', 'darkest red')

    # debug
    if debug:
        show_debug_info(game_map, player, camera, log_frame, ui=True)
    blt.refresh()


def render_obj(coords, dic, camera, color):
    cam_x, cam_y = camera.to_camera_coordinates(coords[0], coords[1])
    map_x, map_y = coords
    blt.color(color)
    blt.puts(cam_x, cam_y, dic.get((map_x, map_y)).char)
    blt.color('white')


def show_debug_info(game_map, player, camera, frame, player_coords=False,
                    mouse_coords=False, ui=False):
    # Show player coords
    blt.color('white')
    if player_coords:
        blt.puts(camera.width, camera.height - 2, str(player.x))
        blt.puts(camera.width, camera.height - 1, str(player.y))
    if ui:
        blt.puts(camera.width + 1, camera.height + 1, 'Total height - height ' + str(frame.contents.total_height - frame.height))
        blt.puts(camera.width + 1, camera.height + 2, 'Offset ' + str(frame.offset))
        blt.puts(camera.width + 1, camera.height + 3, 'Total height ' + str(frame.contents.total_height))
        blt.puts(camera.width + 1, camera.height + 4, 'Num of messages in log ' + str(len(frame.contents.texts)))
        blt.puts(camera.width + 1, camera.height + 5, f'''Scrollbar offset {int(frame.scrollbar_offset / blt.state(blt.TK_CELL_HEIGHT))} = 
        {frame.top} + ({frame.height} - {frame.scrollbar_height}) * (1 - {frame.offset} /
        ({frame.contents.total_height} - {frame.height} + 1))''')

        # Show number of entities around player
    # i = 0
    # for x in range(player.x - 10, player.x + 10):
    #     for y in range(player.y - 10, player.y + 10):
    #         if (x, y) in game_map.entities:
    #             i += 1
    # blt.puts(camera.width, camera.height - 4, str(i))
    if mouse_coords:
        # Show mouse coordinates on map
        mouse_x, mouse_y = camera.to_map_coordinates(blt.state(
            blt.TK_MOUSE_X), blt.state(
            blt.TK_MOUSE_Y))
        blt.puts(camera.width, camera.height - 6, 'Mouse x = ' + str(mouse_x))
        blt.puts(camera.width, camera.height - 5, 'Mouse y = ' + str(mouse_y))
