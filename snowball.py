import pygame as pg
import math
import constants as const

class Snowball(pg.sprite.Sprite):
    def __init__(self, image, start_pos, target):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=start_pos)
        self.target = target
        self.speed = 2.2

    def update(self, level):
        # Aktualizacja pozycji śnieżki w kierunku przeciwnika
        if self.target:
            target_pos = self.target.rect.center
            direction = (target_pos[0] - self.rect.x, target_pos[1] - self.rect.y)
            distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            # Normalizacja kierunku
            if distance != 0:
                direction = (direction[0] / distance, direction[1] / distance)
                self.rect.x += direction[0] * (self.speed * level.speed)
                self.rect.y += direction[1] * (self.speed * level.speed)

            # Sprawdzenie kolizji z przeciwnikiem
            if self.rect.colliderect(self.target.rect):
                self.target.health -= const.DAMAGE
                self.kill()