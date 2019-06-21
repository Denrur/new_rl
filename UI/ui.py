import textwrap

from bearlibterminal import terminal as blt

from game_states import GameStates
from UI.layers import Layers

bar_width = 20
panel_height = 7
panel_y = blt.state(blt.TK_HEIGHT) - panel_height


def ui(game_map, player, camera, game_state, log_frame, action):
    mouse_x, mouse_y = blt.state(blt.TK_MOUSE_X), blt.state(blt.TK_MOUSE_Y)
    names = get_names_under_mouse(game_map.entities, player, camera)

    # print(names)
    if names:
        blt.clear_area(mouse_x + 1, mouse_y, len(names), 1)
        blt.puts(mouse_x + 1, mouse_y, names)
    render_bar(camera.width + 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               'dark red', 'darkest red')

    render_log(1, camera.height + 1, 50, 7, log_frame, action)
    if game_state in (GameStates.SHOW_INVENTORY,
                      GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it'
        else:
            inventory_title = 'Press the key next to an item to drop it'

        inventory_menu(inventory_title,
                       player,
                       50, blt.state(blt.TK_WIDTH),
                       blt.state(blt.TK_HEIGHT))

    blt.layer(Layers.MAP.value)


def render_bar(x, y, total_width, name, value, max_val, foreground, background):
    width = int(float(value) / max_val * total_width)
    blt.layer(Layers.UI_BACKGROUND.value)
    blt.color(background)
    for i in range(total_width):
        blt.puts(x + i, y, f'[color={background}][U+2588]')
    # last_bg = blt.state(blt.TK_BKCOLOR)
    # print('Last_bg', last_bg)
    # blt.color(background)
    # print('Bg', blt.state(blt.TK_BKCOLOR))
    # blt.clear_area(x, y, width, 1)
    # blt.bkcolor(last_bg)
    blt.layer(Layers.UI_FOREGROUND.value)
    if width > 0:
        #last_bg = blt.state(blt.TK_BKCOLOR)
        blt.color(foreground)
        blt.clear_area(x, y, width, 1)
        for i in range(width):
            blt.puts(x + i, y, f'[color={foreground}][U+2588]')

        #blt.bkcolor(last_bg)

    text = name + ':' + str(value) + '/' + str(max_val)
    x_centered = x + (total_width - len(text)) // 2
    blt.layer(Layers.UI_TEXT.value)
    blt.color('white')
    blt.puts(x_centered, y, '[font=small]' + text)
    blt.layer(Layers.UI_BACKGROUND.value)


def render_log(x, y, width, height, log_frame, action=None):
    dragging_scrollbar = False
    dragging_scrollbar_offset = 0
    mouse_scroll_step = 2
    frame = log_frame
    frame.contents.update_heights(width)
    frame.update_geometry(x, y, width, height)
    blt.layer(Layers.UI_BACKGROUND.value)
    scroll = scroll_down = scroll_up = 0
    if action:
        scroll = action.get('scroll')
        scroll_up = action.get('scroll_up')
        scroll_down = action.get('scroll_down')
    if scroll:
        frame.scroll(-1 * mouse_scroll_step * blt.state(blt.TK_MOUSE_WHEEL))
    if scroll_up:
        frame.scroll(-1)
    if scroll_down:
        frame.scroll(1)

    blt.layer(Layers.UI_FOREGROUND.value)
    current_line = frame.height - len(frame.contents.texts)
    # print("----------")
    for text, height in frame.contents:

        # print('Current line', current_line)
        # print('Text', text)
        if current_line + frame.offset < 0:
            pass
        elif current_line + frame.offset > frame.height:
            pass
        else:
            blt.puts(x, y + current_line + frame.offset, text, frame.width)
        current_line += height
        # frame.scrollbar_offset += height * blt.state(blt.TK_CELL_HEIGHT)
    # print(x, y)
    frame.draw()
    # blt.crop(x, y, frame.width, frame.height + 1)


def get_names_under_mouse(entities, player, camera):
    mouse_x, mouse_y = camera.to_map_coordinates(blt.state(
            blt.TK_MOUSE_X), blt.state(
            blt.TK_MOUSE_Y))

    # print(mouse_x, mouse_y)
    # print(entities.get((mouse_x, mouse_y)))
    names = [entity.name for entity in entities.values()
             if entities.get((mouse_x, mouse_y)) == entity and
             (mouse_x, mouse_y) in player.fov.fov_cells]

    names = ', '.join(names)

    return names.capitalize()


def create_window(x, y, w, h, title=None):
    last_bg = blt.state(blt.TK_BKCOLOR)
    blt.bkcolor(blt.color_from_argb(200, 0, 0, 0))
    blt.clear_area(x, y, w + 1, h + 1)
    blt.bkcolor(last_bg)

    border = '[U+250C]' + '[U+2500]' * (w - 2) + '[U+2510]'
    blt.puts(x, y, '[font=small]' + border)
    for i in range(1, h):
        blt.puts(x, y + i, '[font=small][U+2502]')
        blt.puts(x + w - 1, y + i, '[font=small][U+2502]')
    border = '[U+2514]' + '[U+2500]' * (w - 2) + '[U+2518]'
    blt.puts(x, y + h, '[font=small]' + border)

    if title is not None:
        leng = len(title)
        offset = (w + 2 - leng) // 2
        blt.clear_area(x + offset, y, leng, 1)
        blt.puts(x + offset, y, '[font=small]' + title)


def menu(header, options, width, screen_width, screen_height, title=None):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    menu_x = int((screen_width - width) / 2)

    header_wrapped = textwrap.wrap(header, width)
    header_height = len(header_wrapped)

    menu_h = int(header_height + 1 + 26)
    menu_y = int((screen_height - menu_h) / 2)

    create_window(menu_x, menu_y, width, menu_h, title)

    for i, line in enumerate(header_wrapped):
        blt.puts(menu_x + 1, menu_y + 1 + i, header_wrapped[i])

    y = menu_y + header_height + 1
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ')' + option_text
        blt.puts(menu_x + 1, y, text)
        y += 1
        letter_index += 1
    blt.refresh()


def inventory_menu(header, player, inventory_width,
                   screen_width, screen_height):
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            # if player.equipment.main_hand == item:
            #     options.append('{0} (on main hand)'.format(item.name))
            # elif player.equipment.off_hand == item:
            #     options.append('{0} (on off hand)'.format(item.name))
            # else:
            options.append(item.name)

    menu(header, options, inventory_width, screen_width, screen_height,
         title='INVENTORY')