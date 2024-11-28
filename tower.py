import pygame as pg
import math
from snowball import Snowball  # Assuming Snowball is in a separate file
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

class Tower(pg.sprite.Sprite):
    def __init__(self, image, tile_x, tile_y):
        super().__init__()
        self.level = 1
        self.range = const.TOWER_LEVEL[self.level - 1].get("range")
        self.cooldown = const.TOWER_LEVEL[self.level - 1].get("cooldown")
        self.last_snowball = pg.time.get_ticks()
        self.picked = False
        self.target = None

        # Tower position on the grid
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (tile_x + 0.5) * const.TILE_SIZE
        self.y = (tile_y + 0.5) * const.TILE_SIZE

        # Animation and visuals
        self.sprite_sheet = image
        self.frames = load_sprite_sheet(self.sprite_sheet, 64, 64)
        self.frame_index = 0
        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.animation_speed = 0.3
        self.animation_timer = 0
        self.cycle_complete = False
        self.cycle_delay = 1000
        self.cycle_timer = pg.time.get_ticks()
        self.apply_damage = False

        # Targeting and attack
        self.snowball_image = pg.image.load('assets/snowball.png').convert_alpha()
        self.snowball_group = pg.sprite.Group()
        self.current_snowball = None

        # Range display
        self.range_area = pg.Surface((self.range * 2, self.range * 2))
        self.range_area.fill((180, 0, 0))
        self.range_area.set_colorkey((180, 0, 0))
        pg.draw.circle(self.range_area, "black", (self.range, self.range), self.range)
        self.range_area.set_alpha(100)
        self.range_rect = self.range_area.get_rect()
        self.range_rect.center = self.rect.center

        self.snowball_positions = [
            (self.x - 30, self.y + 20),
            (self.x - 30, self.y + 20),
        ]

    def shoot_snowball(self):
        if self.target:
            start_pos = self.snowball_positions[self.frame_index]
            self.current_snowball = Snowball(self.snowball_image, start_pos, self.target)
            self.snowball_group.add(self.current_snowball)

    def animate(self):
        if self.frame_index == 0 and not self.current_snowball:
            self.shoot_snowball()

        if self.cycle_complete:
            if pg.time.get_ticks() - self.cycle_timer >= self.cycle_delay:
                if self.current_snowball:
                    self.current_snowball.fired = True
                    self.current_snowball = None
                self.cycle_complete = False
                self.frame_index = 0
                self.cycle_timer = pg.time.get_ticks()
        else:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames[0])
                if self.frame_index == 0:
                    self.cycle_complete = True
                    self.cycle_timer = pg.time.get_ticks()
                    self.apply_damage = True

                self.image = self.frames[0][self.frame_index]

    def update(self, opponent_group, level):
        if self.target:
            self.animate()
            if self.apply_damage:
                self.apply_damage = False
                self.target = None
        else:
            if pg.time.get_ticks() - self.last_snowball > (self.cooldown / level.speed):
                self.choose_opponent(opponent_group)

        self.snowball_group.update()

    def draw(self, surface):
        # Draw the tower and its active snowballs
        surface.blit(self.image, self.rect)
        self.snowball_group.draw(surface)
        if self.picked:
            surface.blit(self.range_area, self.range_rect)

    def choose_opponent(self, opponent_group):
        for opp in opponent_group:
            if opp.health > 0:
                x_dist = opp.pos[0] - self.x
                y_dist = opp.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = opp
                    break

    def level_up(self):
        self.level += 1
        self.range = const.TOWER_LEVEL[self.level - 1].get("range")
        self.cooldown = const.TOWER_LEVEL[self.level - 1].get("cooldown")

        self.range_area = pg.Surface((self.range * 2, self.range * 2))
        self.range_area.fill((180, 0, 0))
        self.range_area.set_colorkey((180, 0, 0))
        pg.draw.circle(self.range_area, "black", (self.range, self.range), self.range)
        self.range_area.set_alpha(100)
        self.range_rect = self.range_area.get_rect()
        self.range_rect.center = self.rect.center
