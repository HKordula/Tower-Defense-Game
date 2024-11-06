import pygame as pg

class Level():
    def __init__(self, level_img):
        self.image = level_img

    def draw(self, surface):
        surface.blit(self.image, (0, 0))