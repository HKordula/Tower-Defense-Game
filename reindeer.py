import opponent
from opponent import Opponent

class Reindeer(Opponent):
    def __init__(self, routes, sprite_sheet):
        super().__init__(routes, sprite_sheet)
        self.health = 15
        self.speed = 3

        self.speed = 2
        self.frames = opponent.load_sprite_sheet(sprite_sheet, 96, 96)
        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()
        self.animation_speed = 0.15

    def animate(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % 2

        direction_map = {
            'down': 0,
            'left': 1,
            'right': 2,
            'up': 3
        }
        self.image = self.frames[direction_map[self.direction]][self.frame_index]