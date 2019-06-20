from bearlibterminal import terminal as blt
from UI.layers import Layers


bar_width = 20
panel_height = 7
panel_y = blt.state(blt.TK_HEIGHT) - panel_height


def ui(player, camera, log_frame, action):

    render_bar(camera.width + 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               'dark red', 'darkest red')

    render_log(1, camera.height + 1, 50, 7, log_frame, action)

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
    print("----------")
    for text, height in frame.contents:

        print('Current line', current_line)
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


