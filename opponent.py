import pygame as pg
from pygame.math import Vector2


class Opponent(pg.sprite.Sprite):
    def __init__(self, routes, image):
        pg.sprite.Sprite.__init__(self)
        self.routes = routes
        self.pos = Vector2(self.routes[0])
        self.step = 1
        self.speed = 2
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def move(self):
        if self.step < len(self.routes):
            self.target = Vector2(self.routes[self.step])
            self.movement = self.target - self.pos
        else:
            self.kill()

        dist = self.movement.length()
        print(dist)

        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.step += 1

        self.rect.center = self.pos

    def update(self):
        self.move()
