import opponent
from opponent import Opponent
import constants as const

class Reindeer(Opponent):
    def __init__(self, routes, sprite_sheet):
        super().__init__(routes, sprite_sheet)
        self.health = 30
        self.speed = 1.2

        self.frames = opponent.load_sprite_sheet(sprite_sheet, 96, 96)
        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()
        self.animation_speed = 0.15

    def animate(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % 2
        self.image = self.frames[const.DIRECTION_MAP[self.direction]][self.frame_index]