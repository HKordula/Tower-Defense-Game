import pygame as pg

class Button:
    def __init__(self, x, y, image, single_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

        self.states = {
            "default": self.image.subsurface((0, 0, 184, 90)),
            "hover": self.image.subsurface((184, 0, 184, 90)),
            "clicked": self.image.subsurface((2 * 184, 0, 184, 90))
        }
        self.current_image = self.states["default"]

    def draw(self, surface):
        pos = pg.mouse.get_pos()
        action = False

        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.current_image = self.states["clicked"]
                if self.single_click:
                    self.clicked = True
            elif pg.mouse.get_pressed()[0] == 0:
                self.clicked = False
                self.current_image = self.states["hover"]
            else:
                self.current_image = self.states["hover"]
        else:
            self.current_image = self.states["default"]

        surface.blit(self.current_image, self.rect)
        return action