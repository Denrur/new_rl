from bearlibterminal import terminal as blt


def render_all(game_map, player, camera):
    entities = game_map.entities
    terrain = game_map.terrain
    water = game_map.water
    camera.move_camera(player.x, player.y, game_map)

    for x in range(camera.width):
        for y in range(camera.height):
            map_x, map_y = camera.to_map_coordinates(x, y)
            # print('Map_x, map_y', map_x, map_y)
            if (map_x, map_y) in player.fov.fov_cells:
                # print("in fov")
                if (map_x, map_y) in water:
                    render_obj((map_x, map_y), water, camera, 'blue')
                    water.get((map_x, map_y)).explored = True
                if (map_x, map_y) in terrain:
                    # print("in terrain")
                    obj = terrain.get((map_x, map_y))
                    render_obj((map_x, map_y), terrain, camera, obj.color)
                    terrain.get((map_x, map_y)).explored = True
                if (map_x, map_y) in entities:
                    # print("in entites")
                    obj = entities.get((map_x, map_y))
                    render_obj((map_x, map_y), entities, camera, obj.color)
            elif ((map_x, map_y) in terrain and
                    terrain.get((map_x, map_y)).explored):
                render_obj((map_x, map_y), terrain, camera, 'darker orange')
            elif ((map_x, map_y) in water and
                    water.get((map_x, map_y)).explored):
                render_obj((map_x, map_y), water, camera, 'darker blue')
    # debug

    show_debug_info(game_map, player, camera)




def render_obj(coords, dic, camera, color):
    cam_x, cam_y = camera.to_camera_coordinates(coords[0], coords[1])
    map_x, map_y = coords
    blt.color(color)
    blt.puts(cam_x, cam_y, dic.get((map_x, map_y)).char)
    blt.color('white')

def show_debug_info(game_map, player, camera):
    blt.puts(1, camera.height - 2, str(player.x))
    blt.puts(1, camera.height - 1, str(player.y))

    i = 0
    for x in range(player.x - 10, player.x + 10):
        for y in range(player.y - 10, player.y + 10):
            if (x, y) in game_map.terrain:
                i += 1
    blt.puts(1, camera.height - 4, str(i))
    mouse_x, mouse_y = camera.to_map_coordinates(blt.state(
        blt.TK_MOUSE_X), blt.state(
        blt.TK_MOUSE_Y))
    blt.puts(1, camera.height - 6, 'Mouse x = ' + str(mouse_x))
    blt.puts(1, camera.height - 5, 'Mouse y = ' + str(mouse_y))
