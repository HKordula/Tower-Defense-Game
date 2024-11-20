import pygame as pg

import constants as const
from elf import Elf
from level import Level
from reindeer import Reindeer
from santa_claus import SantaClaus
from tower import Tower
from button import Button

pg.init()

clock = pg.time.Clock()

window = pg.display.set_mode((const.WINDOW_WIDTH + const.CONTROL_PANEL, const.WINDOW_HEIGHT))
pg.display.set_caption("Tower Defence Game")

level_image = pg.image.load('assets/map1.png').convert_alpha()
level = Level(level_image)
hitbox_image = pg.image.load('assets/map1hitbox.png').convert_alpha()

tower_image = pg.image.load('assets/tower.png').convert_alpha()
tower_group = pg.sprite.Group()

reindeer_img = pg.image.load('assets/reindeer.png').convert_alpha()
elf_img = pg.image.load('assets/elf.png').convert_alpha()
santa_claus_img = pg.image.load('assets/santa.png').convert_alpha()
opponent_group = pg.sprite.Group()

tower_button_image = pg.image.load('assets/single_tower.png').convert_alpha()
button_group = pg.sprite.Group()

placing = False
picked_tower = None

def placed_tower(position):
    tile_x = position[0] // const.TILE_SIZE
    tile_y = position[1] // const.TILE_SIZE
    free_place = True
    for tow in tower_group:
        if(tile_x, tile_y) == (tow.tile_x, tow.tile_y):
            free_place = False
    color = hitbox_image.get_at((position[0] // const.TILE_SIZE, position[1] // const.TILE_SIZE))
    if free_place and color == (0, 0, 0):
        tower = Tower(tower_image, tile_x, tile_y)
        tower_group.add(tower)
        print(tower_group)

def pick_tower(position):
    tile_x = position[0] // const.TILE_SIZE
    tile_y = position[1] // const.TILE_SIZE
    for tow in tower_group:
        if(tile_x, tile_y) == (tow.tile_x, tow.tile_y):
            return tow

def drop_tower():
    for tow in tower_group:
        tow.picked = False

reindeer = Reindeer(const.routes , reindeer_img)
elf = Elf(const.routes , elf_img)
#santa = SantaClaus(const.routes, santa_claus_img)
opponent_group.add(reindeer)
opponent_group.add(elf)
#opponent_group.add(santa)

tower_button = Button(const.WINDOW_WIDTH + 50, 120, tower_button_image, True)
cancel_button = Button(const.WINDOW_WIDTH + 150, 120, tower_button_image, True)

run = True
while run:

    clock.tick(const.FPS)

    opponent_group.update()
    tower_group.update(opponent_group)

    if picked_tower:
        picked_tower.picked = True

    window.fill('black')

    level.draw(window)

    pg.draw.lines(window, "white", False, const.routes)

    opponent_group.draw(window)
    for tower in tower_group:
        tower.draw(window)

    if tower_button.draw(window):
        placing = True
    if placing:
        cursor_rect = tower_button_image.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= const.WINDOW_WIDTH:
            window.blit(tower_button_image, cursor_rect)
        if cancel_button.draw(window):
            placing = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            position = pg.mouse.get_pos()
            if position[0] < const.WINDOW_WIDTH and position[1] < const.WINDOW_HEIGHT:
                picked_tower = None
                drop_tower()
                if placing:
                    placed_tower(position)
                else:
                    picked_tower = pick_tower(position)

    pg.display.flip()

pg.quit()