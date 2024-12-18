import pygame as pg

import constants as const
from level import Level
from tower import Tower
from utils import load_images, control_panel, create_buttons, write_text

# Inicjalizacja Pygame
pg.init()

# Ustawienie zegara
clock = pg.time.Clock()

# Utworzenie okna, w którym będzie wyświetlana gra
window = pg.display.set_mode((const.WINDOW_WIDTH + const.CONTROL_PANEL, const.WINDOW_HEIGHT))
pg.display.set_caption("Tower Defence Game")

# Załadowanie obrazów do gry
(level_image, hitbox_image, tower_image, snowball_image, opponent_img, opponent_idle_img,
 buy_button_image, upgrade_button_image, cancel_button_image, start_button_image,
 restart_button_image, speed_button_image, tower_mouse_image, level_icon,
 health_icon, money_icon, tower_icon) = load_images()

# Utworzenie instancji klasy Level, przeciwników i wież
level = Level(level_image)
level.spawn_opponents()

tower_group = pg.sprite.Group()
opponent_group = pg.sprite.Group()
button_group = pg.sprite.Group()

# Utworzenie czcionki do wyświetlania tekstu
font = pg.font.SysFont("Courier New ", 60, bold= True)

# Utworzenie przycisków funkcyjnych
buy_button, upgrade_button, cancel_button, start_button, restart_button, speed_button = create_buttons({
    "buy": buy_button_image,
    "upgrade": upgrade_button_image,
    "cancel": cancel_button_image,
    "start": start_button_image,
    "restart": restart_button_image,
    "speed": speed_button_image
})

# Ustawienie zmiennych rozgrywki
start_level = False
game_over = False
game_result = 0
placing = False
picked_tower = None
last_opponent = pg.time.get_ticks()

# Pętla gry
run = True
while run:
    # Ustawienie zeagra
    clock.tick(const.FPS)

    # Logika końca gry
    if not game_over:
        if level.health <= 0:
            game_over = True
            game_result = -1
        if level.level == const.LEVELS and not opponent_group:
            game_over = True
            game_result = 1

        opponent_group.update(level)
        tower_group.update(opponent_group, level)

        if picked_tower:
            picked_tower.picked = True

    # Rysowanie mapy, przeciwników, wież i panelu sterowania
    level.draw(window)
    #pg.draw.lines(window, "white", False, const.routes)

    opponent_group.draw(window)
    for tower in tower_group:
        tower.draw(window)

    control_panel(window, level, font, const, opponent_idle_img, level_icon, health_icon, money_icon, tower_icon)

    if not game_over:
        # Logika startu poziomu
        if not start_level:
            if start_button.draw(window):
                start_level = True
        else:
            # Zmiana prędkości gry
            level.speed = 1
            if speed_button.draw(window):
                level.speed = 1.5

            # Logika pojawiania się przeciwników
            if pg.time.get_ticks() - last_opponent > const.SPAWN_COOLDOWN:
                if level.spawned < len(level.opponent_list):
                    opponent_type = level.opponent_list[level.spawned]
                    opponent = level.get_opponent(opponent_type, const.routes, opponent_img[opponent_type])
                    opponent_group.add(opponent)
                    level.spawned += 1
                    last_opponent = pg.time.get_ticks()

        # Zwiększenie levelu
        if level.level_up():
            start_level = False
            level.level += 1
            last_opponent = pg.time.get_ticks()
            level.reset_stats()
            level.spawn_opponents()
            level.money += const.REWARD

        # Kupowanie i ulepszanie wież
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
        # Ekran końca gry
        pg.draw.rect(window, (92, 0, 0), (const.WINDOW_WIDTH / 2 - 200, const.WINDOW_HEIGHT / 2 - 125, 400, 250), border_radius=30)
        pg.draw.rect(window, "black", (const.WINDOW_WIDTH / 2 - 200, const.WINDOW_HEIGHT / 2 - 125, 400, 250), 5, border_radius=30)
        if game_result == -1:
            write_text(window, "You lose", font, (236, 255, 235), 500, 380)
        elif game_result == 1:
            write_text(window, "You win", font, (236, 255, 235), 515, 380)
        if restart_button.draw(window):
            # Resetowanie gry
            game_over = False
            start_level = False
            placing = False
            picked_tower = None
            last_opponent = pg.time.get_ticks()
            level_image = pg.image.load('assets/map/map1.png').convert_alpha()
            level = Level(level_image)
            hitbox_image = pg.image.load('assets/map/map1hitbox.png').convert_alpha()
            level.spawn_opponents()
            opponent_group.empty()
            tower_group.empty()

    # Obsługa zdarzeń
    for event in pg.event.get():
        # Zamykanie okna
        if event.type == pg.QUIT:
            run = False
        # Wybieranie wieży
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            position = pg.mouse.get_pos()
            if position[0] < const.WINDOW_WIDTH and position[1] < const.WINDOW_HEIGHT:
                picked_tower = None
                Tower.drop_tower(tower_group)
                # Umieszczanie wieży
                if placing:
                    if level.money >= const.TOWER_PRICE:
                        Tower.placed_tower(position,tower_group, hitbox_image, tower_image, level)
                else:
                    picked_tower = Tower.pick_tower(position, tower_group)
    # Odświeżenie okna
    pg.display.flip()

# Zamknięcie Pygame
pg.quit()