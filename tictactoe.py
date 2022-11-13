class Tile:
    
    def __init__(self, pos) -> None:
        self.pos = pos
        self.team = None
        self.clicked = False

    def setClick(self, team):
        if not self.clicked:
            self.clicked = True
            self.team = team
            return True

        return False

class Board:
    pass