import opponent
from opponent import Opponent

class Elf(Opponent):
    def __init__(self, routes, sprite_sheet):
        super().__init__(routes, sprite_sheet)
        self.health = 60
        self.speed = 1

        self.frames = opponent.load_sprite_sheet(sprite_sheet, 64, 64)
        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()
        self.animation_speed = 0.1