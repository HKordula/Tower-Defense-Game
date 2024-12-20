import pygame as pg
from pygame.math import Vector2
import constants as const
from utils import load_sprite_sheet

class Opponent(pg.sprite.Sprite):
    def __init__(self, routes, sprite_sheet):
        pg.sprite.Sprite.__init__(self)
        self.routes = routes
        self.pos = Vector2(self.routes[0])
        self.step = 1
        self.sprite_sheet = sprite_sheet
        self.frames = load_sprite_sheet(sprite_sheet, 64, 64)
        self.direction = 'down'
        self.frame_index = 0
        self.image = self.frames[0][0]
        self.rect = self.image.get_rect(center=self.pos)
        self.animation_timer = 0
        self.spawned = 0

    # Poruszanie się przeciwnika
    def move(self, level):
        # Jeśli przeciwnik nie dotarł do końca trasy
        if self.step < len(self.routes):
            self.target = Vector2(self.routes[self.step])
            self.movement = self.target - self.pos
        else:
            # Jeśli przeciwnik dotarł do końca trasy
            self.kill()
            level.health -= const.PUNISH
            level.missed += 1

        dist = self.movement.length()
        # Jeśli przeciwnik ma jeszcze jakąś drogę do przebycia do kolejnego punktu
        if dist >= (self.speed * level.speed):
            self.pos += self.movement.normalize() * (self.speed * level.speed)
        else:
            # Jeśli przeciwnik jest w punkcie docelowym ustalenie kolejnego punktu docelowego
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.step += 1

        self.rect.center = self.pos

        # Ustalenie kierunku przeciwnika
        if abs(self.movement.x) > abs(self.movement.y):
            self.direction = 'left' if self.movement.x > 0 else 'right'
        else:
            self.direction = 'down' if self.movement.y > 0 else 'up'

    # Animacja przeciwnika
    def animate(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % 4
        self.image = self.frames[const.DIRECTION_MAP[self.direction]][self.frame_index]

    # Aktualizacja przeciwnika
    def update(self, level):
        self.move(level)
        self.animate()
        self.kill_opponent(level)

    # Zabijanie przeciwnika jeżeli jego zdrowie jest mniejsze lub równe 0
    def kill_opponent(self, level):
        if self.health <= 0:
            self.kill()
            level.money += const.BOUNTY
            level.killed +=1