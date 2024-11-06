import pygame as pg

import constants as const
from opponent import Opponent
from level import Level

pg.init()

clock = pg.time.Clock()

window = pg.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
pg.display.set_caption("Tower Defence Game")

level_image = pg.image.load('assets/map1.png').convert_alpha()
level = Level(level_image)

opponent_img = pg.image.load('assets/reindeer1.png').convert_alpha()
opponent_group = pg.sprite.Group()

routes = [
    (128, 0),
    (128, 288),
    (832, 288),
    (832, 128),
    (1152, 128),
    (1152, 800),
    (608, 800),
    (608, 544),
    (416, 544),
    (416, 800),
    (192, 800),
    (192, 608),
    (0, 608)
]

opponent = Opponent(routes , opponent_img)
opponent_group.add(opponent)

run = True
while run:

    clock.tick(const.FPS)

    window.fill('black')

    level.draw(window)

    pg.draw.lines(window, "white", False, routes)

    opponent_group.update()

    opponent_group.draw(window)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()

pg.quit()