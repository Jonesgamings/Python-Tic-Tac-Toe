import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Button:

    def __init__(self, rect: pygame.Rect, text) -> None:
        self.rect = rect
        self.pos = (rect.x, rect.y)
        self.width = rect.width
        self.height = rect.height
        self.colour = (200, 200, 200)
        self.text = text

    def highlighted(self, pos):
        if self.rect.collidepoint(pos):
            self.colour = (100, 100, 100)

        else:
            self.colour = (200, 200, 200)

    def draw(self, screen):
        pygame.draw.rect(screen.screen, self.colour, self.rect)

    def checkClick(self, event):
        if self.rect.collidepoint(event.pos):
            return True

class Tile:
    
    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect
        self.pos = (rect.x, rect.y)
        self.width = rect.width
        self.height = rect.height
        self.team = None
        self.clicked = False

    def checkClick(self, event, team):
        if team != "AI":
            if self.rect.collidepoint(event.pos):
                if not self.clicked:
                    self.clicked = True
                    self.team = team
                    return 1

        return 0

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
        self.visible = False
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

    def checkForWin(self):
        pass

    def doAIMove(self):
        if self.currentTeam == "AI":
            self.switchTeams()

    def update(self):
        self.checkForWin()

        if self.gameType == BoardWindow.AI:
            self.doAIMove()

    def switchTeams(self):
        if self.currentTeam == "P1":
            self.currentTeam == "P2"

        elif self.currentTeam == "P2":
            self.currentTeam == "P1"

        elif self.currentTeam == "AI":
            self.currentTeam == "PLAYER"

        elif self.currentTeam == "PLAYER":
            self.currentTeam == "AI"

    def event(self, event):
        switch = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            for tile in self.tiles.values():
                switch += tile.checkClick(event, self.currentTeam)

        if switch > 0:
            self.switchTeams()

class MainMenu:

    def __init__(self, screen) -> None:
        self.screen: Screen = screen
        self.visible = True
        self.AIButton = Button(pygame.Rect(100, 100, 100, 100), "AI")
        self.PlayerButton = Button(pygame.Rect(250, 100, 100, 100), "PLAYER")

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.AIButton.highlighted(mousePos)
        self.PlayerButton.highlighted(mousePos)

    def draw(self):
        self.AIButton.draw(self.screen)
        self.PlayerButton.draw(self.screen)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.AIButton.checkClick(event):
                self.screen.loadGame(BoardWindow.AI)

            elif self.PlayerButton.checkClick(event):
                self.screen.loadGame(BoardWindow.PLAYER)

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
            self.mainmanu.update()
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
        self.unloadGame()
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