from opponent import Opponent

class Elf(Opponent):
    def __init__(self, routes, sprite_sheet):
        super().__init__(routes, sprite_sheet)
        self.health = 10
        self.speed = 2
        self.spawned = 0

