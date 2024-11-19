from opponent import Opponent

class SantaClaus(Opponent):
    def __init__(self, routes, sprite_sheet):
        super().__init__(routes, sprite_sheet)
        self.speed = 0.75