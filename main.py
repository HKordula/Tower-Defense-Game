import pygame as pg

import constants
import constants as const
from opponent import Opponent
from level import Level
from tower import Tower

pg.init()

clock = pg.time.Clock()

window = pg.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
pg.display.set_caption("Tower Defence Game")

level_image = pg.image.load('assets/map1.png').convert_alpha()
level = Level(level_image)
hitbox_image = pg.image.load('assets/map1hitbox.png').convert_alpha()

tower_image = pg.image.load('assets/elf1.png').convert_alpha()
tower_group = pg.sprite.Group()

opponent_img = pg.image.load('assets/elf.png').convert_alpha()
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

def placed_tower(position):
    tile_x = position[0] // const.TILE_SIZE
    tile_y = position[1] // const.TILE_SIZE
    free_place = True
    for tow in tower_group:
        if(tile_x, tile_y) == (tow.tile_x, tow.tile_y):
            free_place = False
    color = hitbox_image.get_at((position[0] // const.TILE_SIZE, position[1] // const.TILE_SIZE))
    if color == (0, 0, 0):
        if free_place:
            tower = Tower(tower_image, tile_x, tile_y)
            tower_group.add(tower)
            print(tower_group)

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
    tower_group.draw(window)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            position = pg.mouse.get_pos()
            if(position[0] < constants.WINDOW_WIDTH and position[1] < constants.WINDOW_HEIGHT):
                placed_tower(position)

    pg.display.flip()

pg.quit()