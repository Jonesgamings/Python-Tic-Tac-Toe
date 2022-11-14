import pygame

class Tile:
    
    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect
        self.pos = (rect.x, rect.y)
        self.width = rect.width
        self.height = rect.height
        self.team = None
        self.clicked = False

    def setClick(self, team):
        if not self.clicked:
            self.clicked = True
            self.team = team
            return True

        return False

class BoardWindow:

    AI = "AI"
    PLAYER = "PLAYER"
    
    def __init__(self, screen, size, offset) -> None:
        self.screen: Screen = screen
        self.visible = False
        self.size = size
        self.tiles = {}
        self.gridX = 0
        self.gridY = 0
        self.offset = offset

    def generateBlank(self):

        self.gridX = ((self.screen.width) / self.size) - (self.offset / self.size * 2)
        self.gridY = ((self.screen.height) / self.size) - (self.offset / self.size * 2)

        for y in range(self.size):
            for x in range(self.size):
                pos = (y, x)
                rect = pygame.rect(self.gridX * x, self.gridY * y, self.gridX, self.gridY)
                tile = Tile(rect)
                self.tiles[pos] = tile

    def draw(self):
        pass

    def event(self, event):
        pass

class MainMenu:

    def __init__(self, screen) -> None:
        self.screen = screen
        self.visible = False

    def draw(self):
        pass

    def event(self, event):
        pass

class Screen:

    def __init__(self, width, height) -> None:
        self.boardSize = 3
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        self.boardWindow = BoardWindow(self, self.boardSize, 30)
        self.mainmanu = MainMenu(self)

    def update(self):
        if self.boardWindow.visible:
            self.boardWindow.draw()

        if self.mainmanu.visible:
            self.mainmanu.draw()

    def sendEvent(self, event):
        if self.boardWindow.visible:
            self.boardWindow.event(event)

        if self.mainmanu.visible:
            self.mainmanu.event(event)