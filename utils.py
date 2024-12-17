import pygame as pg

from button import Button
import constants as const

def load_sprite_sheet(sheet, frame_width, frame_height):
    sheet_rect = sheet.get_rect()
    sprites = []
    for row in range(sheet_rect.height // frame_height):
        row_sprites = []
        for col in range(sheet_rect.width // frame_width):
            frame = sheet.subsurface(pg.Rect(col * frame_width, row * frame_height, frame_width, frame_height))
            row_sprites.append(frame)
        sprites.append(row_sprites)
    return sprites

def load_images():
    try:
        level_image = pg.image.load('assets/map/map1.png').convert_alpha()
        hitbox_image = pg.image.load('assets/map/map1hitbox.png').convert_alpha()
        tower_image = pg.image.load('assets/towers/tower.png').convert_alpha()
        snowball_image = pg.image.load('assets/towers/snowball.png').convert_alpha()
        opponent_img = {
            "elf": pg.image.load('assets/opponents/elf.png').convert_alpha(),
            "reindeer": pg.image.load('assets/opponents/reindeer.png').convert_alpha(),
            "santa_claus": pg.image.load('assets/opponents/santa.png').convert_alpha()
        }
        opponent_idle_img = {
            "elf": pg.image.load('assets/opponents/elf-idle.png').convert_alpha(),
            "reindeer": pg.image.load('assets/opponents/reindeer-idle.png').convert_alpha(),
            "santa_claus": pg.image.load('assets/opponents/santa-idle.png').convert_alpha()
        }
        button_images = {
            "buy": pg.image.load('assets/buttons/buy.png').convert_alpha(),
            "upgrade": pg.image.load('assets/buttons/upgrade.png').convert_alpha(),
            "cancel": pg.image.load('assets/buttons/cancel.png').convert_alpha(),
            "start": pg.image.load('assets/buttons/start.png').convert_alpha(),
            "restart": pg.image.load('assets/buttons/restart.png').convert_alpha(),
            "speed": pg.image.load('assets/buttons/speed.png').convert_alpha()
        }
        tower_mouse_image = pg.image.load('assets/towers/single_tower.png').convert_alpha()
        icons = {
            "level": pg.image.load('assets/icons/star.png').convert_alpha(),
            "health": pg.image.load('assets/icons/health.png').convert_alpha(),
            "money": pg.image.load('assets/icons/gift.png').convert_alpha(),
            "tower": pg.image.load('assets/icons/santa_hat.png').convert_alpha()
        }
        return (level_image, hitbox_image, tower_image, snowball_image, opponent_img, opponent_idle_img,
                button_images["buy"], button_images["upgrade"], button_images["cancel"], button_images["start"],
                button_images["restart"], button_images["speed"], tower_mouse_image, icons["level"],
                icons["health"], icons["money"], icons["tower"])
    except FileNotFoundError as e:
        print(f"Error loading images: {e}")
        pg.quit()
        exit()

def control_panel(window, level, font, const, opponent_idle_img, level_icon, health_icon, money_icon, tower_icon):
    pg.draw.rect(window, (92, 0, 0), (const.WINDOW_WIDTH, 0, const.CONTROL_PANEL, const.WINDOW_HEIGHT))
    pg.draw.rect(window, "black", (const.WINDOW_WIDTH, 0, const.CONTROL_PANEL, const.WINDOW_HEIGHT), 5)

    write_text(window, str(level.level) + "/" + str(const.LEVELS), font, (236, 255, 235), const.WINDOW_WIDTH + 100, 15)
    window.blit(level_icon, (const.WINDOW_WIDTH + 20, 10))
    write_text(window, str(level.health), font, (236, 255, 235), const.WINDOW_WIDTH + 100, 100)
    window.blit(health_icon, (const.WINDOW_WIDTH + 20, 100))
    write_text(window, str(level.money), font, (236, 255, 235), const.WINDOW_WIDTH + 330, 100)
    window.blit(money_icon, (const.WINDOW_WIDTH + 250, 100))

    window.blit(tower_icon, (const.WINDOW_WIDTH + 20, 220))
    write_text(window, str(const.TOWER_PRICE), font, (236, 255, 235), const.WINDOW_WIDTH + 310, 225)
    window.blit(money_icon, (const.WINDOW_WIDTH + 420, 220))

    wave_data = const.WAVES_DATA[level.level - 1]
    opponent_counts = list(wave_data.values())

    write_text(window, "Opponents", font, (236, 255, 235), const.WINDOW_WIDTH + 90, 770)
    window.blit(opponent_idle_img["elf"], (const.WINDOW_WIDTH + 25, 850))
    write_text(window, str(opponent_counts[0]), font, (236, 255, 235), const.WINDOW_WIDTH + 95, 860)
    window.blit(opponent_idle_img["reindeer"], (const.WINDOW_WIDTH + 175, 834))
    write_text(window, str(opponent_counts[1]), font, (236, 255, 235), const.WINDOW_WIDTH + 245, 860)
    window.blit(opponent_idle_img["santa_claus"], (const.WINDOW_WIDTH + 325, 850))
    write_text(window, str(opponent_counts[2]), font, (236, 255, 235), const.WINDOW_WIDTH + 395, 860)

def write_text(window, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

def create_buttons(button_images):
    buy_button = Button(const.WINDOW_WIDTH + 100, 210, button_images["buy"], True)
    upgrade_button = Button(const.WINDOW_WIDTH + 100, 210, button_images["upgrade"], True)
    cancel_button = Button(const.WINDOW_WIDTH + 100, 310, button_images["cancel"], True)
    start_button = Button(const.WINDOW_WIDTH + 150, 420, button_images["start"], True)
    restart_button = Button(550, 480, button_images["restart"], True)
    speed_button = Button(const.WINDOW_WIDTH + 150, 420, button_images["speed"], False)
    return buy_button, upgrade_button, cancel_button, start_button, restart_button, speed_button