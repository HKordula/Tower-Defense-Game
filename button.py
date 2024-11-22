import pygame as pg

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.hovered = False

        self.states = {
            "default": self.image.subsurface((0, 0, 184, 90)),
            "hover": self.image.subsurface((184, 0, 184, 90)),
            "clicked": self.image.subsurface((2 * 184, 0, 184, 90))
        }
        self.current_image = self.states["default"]

    def draw(self, surface):
        action = False
        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.hovered = True
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.current_image = self.states["clicked"]
                action = True
            elif pg.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
        else:
            self.hovered = False

        if not self.clicked:
            if self.hovered:
                self.current_image = self.states["hover"]
            else:
                self.current_image = self.states["default"]

        surface.blit(self.current_image, (self.rect.x, self.rect.y))
        return action