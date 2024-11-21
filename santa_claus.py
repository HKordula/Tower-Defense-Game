from opponent import Opponent

class SantaClaus(Opponent):
    def __init__(self, routes, sprite_sheet):
        super().__init__(routes, sprite_sheet)
        self.health = 50
        self.speed = 1