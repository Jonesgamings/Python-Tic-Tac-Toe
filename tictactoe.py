import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Tile:
    
    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect
        self.pos = (rect.x, rect.y)
        self.width = rect.width
        self.height = rect.height
        self.team = None
        self.clicked = False

    def checkClick(self, event, team):
        if self.rect.collidepoint(event.pos):
            if not self.clicked:
                self.clicked = True
                self.team = team

    def draw(self, screen):
        if not self.clicked:
            pygame.draw.rect(screen, BLACK, self.rect, 3)

        else:
            pygame.draw.rect(screen, BLACK, self.rect)

class BoardWindow:

    AI = "AI"
    PLAYER = "PLAYER"
    
    def __init__(self, screen, size, offset) -> None:
        self.screen: Screen = screen
        self.visible = True
        self.size = size
        self.tiles = {}
        self.gridX = 0
        self.gridY = 0
        self.offset = offset
        self.gameType = None
        self.currentTeam = None
        
        self.generateBlank()

    def generateBlank(self):

        self.gridX = ((self.screen.width) / self.size) - (self.offset / self.size * 2)
        self.gridY = ((self.screen.height) / self.size) - (self.offset / self.size * 2)

        for y in range(self.size):
            for x in range(self.size):
                pos = (y, x)
                realX = self.gridX * x + self.offset
                realY = self.gridY * y + self.offset
                rect = pygame.Rect(realX, realY, self.gridX, self.gridY)
                tile = Tile(rect)
                self.tiles[pos] = tile

    def startGame(self, type_):
        self.visible = True
        self.gameType = type_
        self.currentTeam = 1

    def endGame(self):
        self.visible = False
        self.gameType = None
        self.currentTeam = None

    def draw(self):
        for tile in self.tiles.values():
            tile.draw(self.screen.screen)

    def update(self):
        pass

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for tile in self.tiles.values():
                tile.checkClick(event, self.currentTeam)

class MainMenu:

    def __init__(self, screen) -> None:
        self.screen = screen
        self.visible = False
        #self.AIButton = pygame.Rect()
        #self.PlayerButton = pygame.Rect()

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
        self.running = False

    def update(self):
        self.screen.fill(WHITE)
        if self.boardWindow.visible:
            self.boardWindow.update()
            self.boardWindow.draw()

        if self.mainmanu.visible:
            self.mainmanu.draw()

    def sendEvent(self, event):
        if self.boardWindow.visible:
            self.boardWindow.event(event)

        if self.mainmanu.visible:
            self.mainmanu.event(event)

    def loadGame(self, type_):
        self.unloadMenu()
        self.boardWindow.startGame(type_)

    def unloadGame(self):
        self.boardWindow.endGame()

    def loadMenu(self):
        self.mainmanu.visible = True

    def unloadMenu(self):
        self.mainmanu.visible = False

    def mainloop(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.sendEvent(event)

            self.update()

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    screen = Screen(1000, 1000)
    screen.mainloop()