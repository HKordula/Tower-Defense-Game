import pygame as pg
from pygame.math import Vector2

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

class Opponent(pg.sprite.Sprite):
    def __init__(self, routes, sprite_sheet):
        pg.sprite.Sprite.__init__(self)
        self.routes = routes
        self.pos = Vector2(self.routes[0])
        self.step = 1
        self.speed = 2
        self.sprite_sheet = sprite_sheet
        self.frames = load_sprite_sheet(sprite_sheet, 64, 64)
        self.direction = 'down'
        self.frame_index = 0
        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.animation_speed = 0.1
        self.animation_timer = 0

    def move(self):
        if self.step < len(self.routes):
            self.target = Vector2(self.routes[self.step])
            self.movement = self.target - self.pos
        else:
            self.kill()

        dist = self.movement.length()

        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.step += 1

        self.rect.center = self.pos

        if abs(self.movement.x) > abs(self.movement.y):
            if self.movement.x > 0:
                self.direction = 'left'
            else:
                self.direction = 'right'
        else:
            if self.movement.y > 0:
                self.direction = 'down'
            else:
                self.direction = 'up'

    def animate(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % 4

        direction_map = {
            'down': 0,
            'left': 1,
            'right': 2,
            'up': 3
        }
        self.image = self.frames[direction_map[self.direction]][self.frame_index]

    def update(self):
        self.move()
        self.animate()