import pygame as pg
import math

from utils import load_sprite_sheet
from snowball import Snowball
import constants as const

class Tower(pg.sprite.Sprite):
    def __init__(self, image, tile_x, tile_y):
        super().__init__()
        self.level = 1
        self.range = const.TOWER_LEVEL[self.level - 1].get("range")
        self.cooldown = const.TOWER_LEVEL[self.level - 1].get("cooldown")
        self.last_snowball = pg.time.get_ticks()
        self.picked = False
        self.target = None

        self.x = (tile_x + 0.5) * const.TILE_SIZE
        self.y = (tile_y + 0.5) * const.TILE_SIZE

        self.frames = load_sprite_sheet(image, 64, 64)
        self.frame_index = 0
        self.image = self.frames[0][0]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.animation_speed = 0.3
        self.animation_timer = 0
        self.cycle_complete = False
        self.cycle_delay = 1000
        self.cycle_timer = pg.time.get_ticks()
        self.apply_damage = False

        self.snowball_image = pg.image.load('assets/towers/snowball.png').convert_alpha()
        self.snowball_group = pg.sprite.Group()
        self.current_snowball = None

        self.range_area = pg.Surface((self.range * 2, self.range * 2))
        self.range_area.fill((180, 0, 0))
        self.range_area.set_colorkey((180, 0, 0))
        pg.draw.circle(self.range_area, "black", (self.range, self.range), self.range)
        self.range_area.set_alpha(100)
        self.range_rect = self.range_area.get_rect()
        self.range_rect.center = self.rect.center

    # Strzelanie śnieżką
    def shoot_snowball(self):
        if self.target:
            start_pos = (self.x - 30, self.y + 20)
            self.current_snowball = Snowball(self.snowball_image, start_pos, self.target)
            self.snowball_group.add(self.current_snowball)

    # Animacja wieży
    def animate(self):
        # Rozpoczęcie strzelania
        if self.frame_index == 0 and not self.current_snowball:
            self.shoot_snowball()

        # Sprawdzenie czy cykl animacji się zakończył
        if self.cycle_complete:
            # Sprawdzenie czy minął czas od zakończenia cyklu
            if pg.time.get_ticks() - self.cycle_timer >= self.cycle_delay:
                if self.current_snowball:
                    self.current_snowball.fired = True
                    self.current_snowball = None
                self.cycle_complete = False
                self.frame_index = 0
                self.cycle_timer = pg.time.get_ticks()
        else:
            # Animacja wieży
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames[0])
                if self.frame_index == 0:
                    self.cycle_complete = True
                    self.cycle_timer = pg.time.get_ticks()
                    self.apply_damage = True

                self.image = self.frames[0][self.frame_index]

    # Aktualizacja stanu wieży
    def update(self, opponent_group, level):
        if self.target:
            self.animate()
            if self.apply_damage:
                self.apply_damage = False
                self.target = None
        else:
            if pg.time.get_ticks() - self.last_snowball > (self.cooldown / level.speed):
                self.choose_opponent(opponent_group)

        self.snowball_group.update(level)

    # Rysowanie wieży na ekranie
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.snowball_group.draw(surface)
        if self.picked:
            surface.blit(self.range_area, self.range_rect)

    # Wybór przeciwnika, którego wieża będzie atakować
    def choose_opponent(self, opponent_group):
        for opp in opponent_group:
            if opp.health > 0:
                x_dist = opp.pos[0] - self.x
                y_dist = opp.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = opp
                    break

    # Zwiększenie poziomu wieży
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

    # Funkcja do umieszczania wieży
    @staticmethod
    def placed_tower(position, tower_group, hitbox_image, tower_image, level):
        tile_x, tile_y = position[0] // const.TILE_SIZE, position[1] // const.TILE_SIZE
        free_place = True
        for tow in tower_group:
            if (tile_x, tile_y) == (tow.tile_x, tow.tile_y):
                free_place = False
        color = hitbox_image.get_at((position[0] // const.TILE_SIZE, position[1] // const.TILE_SIZE))
        if free_place and color == (0, 0, 0):
            tower = Tower(tower_image, tile_x, tile_y)
            tower_group.add(tower)
            level.money -= const.TOWER_PRICE

    # Funcja do wyboru wieży
    @staticmethod
    def pick_tower(position, tower_group):
        tile_x, tile_y = position[0] // const.TILE_SIZE, position[1] // const.TILE_SIZE
        for tow in tower_group:
            if (tile_x, tile_y) == (tow.tile_x, tow.tile_y):
                return tow

    # Funkcja do anulowania wyboru wieży
    @staticmethod
    def drop_tower(tower_group):
        for tow in tower_group:
            tow.picked = False