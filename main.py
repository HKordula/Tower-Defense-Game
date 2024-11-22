import pygame as pg

import constants as const
from level import Level
from tower import Tower
from button import Button

pg.init()

clock = pg.time.Clock()

window = pg.display.set_mode((const.WINDOW_WIDTH + const.CONTROL_PANEL, const.WINDOW_HEIGHT))
pg.display.set_caption("Tower Defence Game")

level_image = pg.image.load('assets/map1.png').convert_alpha()
level = Level(level_image)
hitbox_image = pg.image.load('assets/map1hitbox.png').convert_alpha()
level.spawn_opponents()

tower_image = pg.image.load('assets/tower.png').convert_alpha()
tower_group = pg.sprite.Group()

opponent_img = {
    "elf": pg.image.load('assets/elf.png').convert_alpha(),
    "reindeer": pg.image.load('assets/reindeer.png').convert_alpha(),
    "santa_claus": pg.image.load('assets/santa.png').convert_alpha()
}

opponent_group = pg.sprite.Group()

buy_button_image = pg.image.load('assets/buttons/buy.png').convert_alpha()
upgrade_button_image = pg.image.load('assets/buttons/upgrade.png').convert_alpha()
cancel_button_image = pg.image.load('assets/buttons/cancel.png').convert_alpha()
start_button_image = pg.image.load('assets/buttons/start.png').convert_alpha()
restart_button_image = pg.image.load('assets/buttons/restart.png').convert_alpha()
speed_button_image = pg.image.load('assets/buttons/speed.png').convert_alpha()
button_group = pg.sprite.Group()

tower_mouse_image = pg.image.load('assets/single_tower.png').convert_alpha()

level_icon = pg.image.load('assets/icons/star.png').convert_alpha()
health_icon = pg.image.load('assets/icons/health.png').convert_alpha()
money_icon = pg.image.load('assets/icons/gift.png').convert_alpha()
tower_icon = pg.image.load('assets/icons/santa_hat.png').convert_alpha()

#music = pg.mixer.Sound('assets/music.wav')
#music.set_volume(0.1)

font = pg.font.SysFont("Courier New ", 60, bold= True)

start_level = False
game_over = False
game_result = 0
placing = False
picked_tower = None
last_opponent = pg.time.get_ticks()

def control_panel():
    pg.draw.rect(window, (92, 0, 0), (const.WINDOW_WIDTH, 0, const.CONTROL_PANEL, const.WINDOW_HEIGHT))
    pg.draw.rect(window, "black", (const.WINDOW_WIDTH, 0, const.CONTROL_PANEL, const.WINDOW_HEIGHT), 5)

    write_text(str(level.level), font, (236, 255, 235), const.WINDOW_WIDTH + 100, 15)
    window.blit(level_icon, (const.WINDOW_WIDTH + 20, 10))
    write_text(str(level.health), font, (236, 255, 235), const.WINDOW_WIDTH + 100, 100)
    window.blit(health_icon, (const.WINDOW_WIDTH + 20, 100))
    write_text(str(level.money), font, (236, 255, 235), const.WINDOW_WIDTH + 330, 100)
    window.blit(money_icon, (const.WINDOW_WIDTH + 250, 100))

    window.blit(tower_icon, (const.WINDOW_WIDTH + 20, 220))
    write_text(str(const.TOWER_PRICE), font, (236, 255, 235), const.WINDOW_WIDTH + 310, 225)
    window.blit(money_icon, (const.WINDOW_WIDTH + 420, 220))


def write_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

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
        level.money -= const.TOWER_PRICE
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


buy_button = Button(const.WINDOW_WIDTH + 100, 210, buy_button_image, True)
upgrade_button = Button(const.WINDOW_WIDTH + 100, 260, upgrade_button_image, True)
cancel_button = Button(const.WINDOW_WIDTH + 100, 310, cancel_button_image, True)
start_button = Button(const.WINDOW_WIDTH + 150, 420, start_button_image, True)
restart_button = Button(350, 160, restart_button_image, True)
speed_button = Button(const.WINDOW_WIDTH + 350, 200, speed_button_image, True)

#music.play()

run = True
while run:

    clock.tick(const.FPS)

    if game_over == False:
        if level.health <= 0:
            game_over = True
            game_result = -1
        if level.level > const.LEVELS:
            game_over = True
            game_result = 1

        opponent_group.update(level)
        tower_group.update(opponent_group, level)

        if picked_tower:
            picked_tower.picked = True

    level.draw(window)

    pg.draw.lines(window, "white", False, const.routes)

    opponent_group.draw(window)
    for tower in tower_group:
        tower.draw(window)

    control_panel()

    if game_over == False:
        if start_level == False:
            if start_button.draw(window):
                start_level = True
        else:
            level.speed = 1
            if speed_button.draw(window):
                level.speed = 2

            if pg.time.get_ticks() - last_opponent > const.SPAWN_COOLDOWN:
                if level.spawned < len(level.opponent_list):
                    opponent_type = level.opponent_list[level.spawned]
                    opponent = level.get_opponent(opponent_type, const.routes, opponent_img[opponent_type])
                    opponent_group.add(opponent)
                    level.spawned += 1
                    last_opponent = pg.time.get_ticks()

        if level.level_up() == True:
            start_level = False
            level.level += 1
            last_opponent = pg.time.get_ticks()
            level.reset_stats()
            level.spawn_opponents()
            level.money += const.REWARD

        if buy_button.draw(window):
            placing = True
        if placing:
            cursor_rect = tower_mouse_image.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= const.WINDOW_WIDTH:
                window.blit(tower_mouse_image, cursor_rect)
            if cancel_button.draw(window):
                placing = False
        if picked_tower:
            if picked_tower.level < const.MAX_LEVEL:
                if upgrade_button.draw(window):
                    if level.money >= const.TOWER_UPGRADE:
                        picked_tower.level_up()
                        level.money -= const.TOWER_UPGRADE
    else:
        pg.draw.rect(window, "green", (200, 200, 400, 200) , border_radius=30)
        if game_result == -1:
            write_text("You lose", font, "red", 310, 230)
        elif game_result == 1:
            write_text("You win", font, "red", 310, 230)
        if restart_button.draw(window):
            game_over = False
            start_level = False
            placing = False
            picked_tower = None
            last_opponent = pg.time.get_ticks()
            level_image = pg.image.load('assets/map1.png').convert_alpha()
            level = Level(level_image)
            hitbox_image = pg.image.load('assets/map1hitbox.png').convert_alpha()
            level.spawn_opponents()
            opponent_group.empty()
            tower_group.empty()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            position = pg.mouse.get_pos()
            if position[0] < const.WINDOW_WIDTH and position[1] < const.WINDOW_HEIGHT:
                picked_tower = None
                drop_tower()
                if placing:
                    if level.money >= const.TOWER_PRICE:
                        placed_tower(position)
                else:
                    picked_tower = pick_tower(position)

    pg.display.flip()

pg.quit()