import pygame as pg

class Button:
    def __init__(self, x, y, image, single_click):
        # Inicjalizacja przycisku
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.single_click = single_click

        # Definiowanie stanów przycisku
        self.states = {
            "default": self.image.subsurface((0, 0, 184, 90)),
            "hover": self.image.subsurface((184, 0, 184, 90)),
            "clicked": self.image.subsurface((2 * 184, 0, 184, 90))
        }
        self.current_image = self.states["default"]

    def draw(self, surface):
        # Rysowanie przycisku
        pos = pg.mouse.get_pos()
        action = False

        # Obsługa zdarzeń myszy
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                if not self.clicked:
                    action = True
                    self.current_image = self.states["clicked"]
                    if self.single_click:
                        self.clicked = True
            else:
                self.clicked = False
                self.current_image = self.states["hover"]
        else:
            self.current_image = self.states["default"]

        # Rysowanie aktualnego stanu przycisku
        surface.blit(self.current_image, self.rect)
        return action