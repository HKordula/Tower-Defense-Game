import pygame as pg
from pygame.examples.go_over_there import screen

import constants as const
from opponent import Opponent

pg.init()

clock = pg.time.Clock()

window = pg.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
pg.display.set_caption("Tower Defence Game")

opponent_img = pg.image.load('assets/elf1.png').convert_alpha()

opponent_group = pg.sprite.Group()

opponent = Opponent((200, 300) , opponent_img)
opponent_group.add(opponent)

run = True
while run:

    clock.tick(const.FPS)

    window.fill('black')

    opponent_group.update()

    opponent_group.draw(window)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()

pg.quit()