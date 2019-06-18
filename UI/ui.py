from bearlibterminal import terminal as blt
from UI.layers import Layers


bar_width = 20
panel_height = 7
panel_y = blt.state(blt.TK_HEIGHT) - panel_height


def ui(player, camera):
    blt.layer(Layers.UI_BACKGROUND.value)
    print(Layers.UI_BACKGROUND.value)
    render_bar(camera.width + 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               'dark red', 'darkest red')
    print('UI layer', blt.state(blt.TK_LAYER))
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

