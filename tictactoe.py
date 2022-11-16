import pygame

pygame.font.init()
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Button:

    def __init__(self, rect: pygame.Rect, text, font) -> None:
        self.rect = rect
        self.pos = (rect.x, rect.y)
        self.width = rect.width
        self.height = rect.height
        self.colour = (200, 200, 200)
        self.text = text
        self.font = font

    def highlighted(self, pos):
        if self.rect.collidepoint(pos):
            self.colour = (100, 100, 100)

        else:
            self.colour = (200, 200, 200)

    def draw(self, screen):
        textSurf = self.font.render(self.text, False, BLACK)
        size = self.font.size(self.text)
        textPos = (((self.pos[0]) - size[0] / 2) + self.width / 2, ((self.pos[1]) - size[1] / 2) + self.height / 2)
        pygame.draw.rect(screen.screen, self.colour, self.rect)
        screen.screen.blit(textSurf, textPos)


    def checkClick(self, event):
        if self.rect.collidepoint(event.pos):
            return 1

        return 0

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
        screen = screen.screen
        if self.team:
            if self.team == "PLAYER" or self.team == "P1":
                pygame.draw.line(screen, BLACK, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), 3)
                pygame.draw.line(screen, BLACK, (self.pos[0], self.pos[1] + self.height), (self.pos[0] + self.width, self.pos[1]), 3)

            elif self.team == "AI" or self.team == "P2":
                pygame.draw.circle(screen, BLACK, (self.pos[0] + self.width / 2, self.pos[1] + self.height / 2), self.width / 2, 3)

        pygame.draw.rect(screen, BLACK, self.rect, 3)

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

        self.createButtons()
        self.generateBlank()

    def createButtons(self):
        width = self.screen.width / 6
        height = self.screen.height / 24
        font = pygame.font.SysFont("Comic Sans MS", 30)

        self.quitButton = Button(pygame.Rect(0, self.screen.height - height, width, height), "QUIT", font)

    def generateBlank(self):

        self.gridX = ((self.screen.width) / self.size) - (self.offset / self.size * 2)
        self.gridY = ((self.screen.height) / self.size) - (self.offset / self.size * 2)

        for y in range(self.size):
            for x in range(self.size):
                pos = (x, y)
                realX = self.gridX * x + self.offset
                realY = self.gridY * y + self.offset
                rect = pygame.Rect(realX, realY, self.gridX, self.gridY)
                tile = Tile(rect)
                self.tiles[pos] = tile

    def startGame(self, type_):
        self.visible = True
        self.gameType = type_
        self.currentTeam = 1

        if type_ == BoardWindow.AI:
            self.currentTeam = "PLAYER"

        elif type_ == BoardWindow.PLAYER:
            self.currentTeam = "P1"

        self.generateBlank()

    def endGame(self):
        self.visible = False
        self.gameType = None
        self.currentTeam = None
        self.screen.loadMenu()

    def win(self, team):
        if team != "DRAW": text = f"{team} WINS"
        else: text = "DRAW" 

        for tile in self.tiles.values():
            tile.clicked = True
        
        font = pygame.font.SysFont("Comic Sans MS", 30)
        size = font.size(text)
        textPos = ((self.screen.width / 2), self.screen.height - size[1] / 2)
        self.displayText(font, size, text, textPos)

    def displayText(self, font, size, text, pos):
        textSurf = font.render(text, False, BLACK)
        textPos = (pos[0] - size[0] / 2, pos[1] - size[1] / 2)
        self.screen.screen.blit(textSurf, textPos)

    def draw(self):
        for tile in self.tiles.values():
            tile.draw(self.screen)

        font = pygame.font.SysFont("Comic Sans MS", 30)
        size = font.size(self.currentTeam)
        textPos = (size[0] / 2, size[1] / 2)

        self.displayText(font, size, self.currentTeam, textPos)
        self.quitButton.draw(self.screen)

    def checkForWin(self):
        diagL = set()
        diagR = set()
        countDL = 0
        countDR = 0
        GENCOUNT = 0
        for y in range(self.size):
            rows = set()
            columns = set()
            countR = 0
            countC = 0
            for x in range(self.size):
                teamR = self.tiles[x, y].team
                teamC = self.tiles[y, x].team
                if teamR:
                    rows.add(teamR)
                    countR += 1
                    GENCOUNT += 1

                if teamC:
                    columns.add(teamC)
                    countC += 1

                if teamR:
                    if x == y:
                        diagL.add(teamR)
                        countDL += 1

                    if x == self.size - 1 - y:
                        diagR.add(teamR)
                        countDR += 1

            if len(rows) == 1:
                if countR == self.size:
                    return list(rows)[0]

            if len(columns) == 1:
                if countC == self.size:
                    return list(columns)[0]

        if len(diagL) == 1:
            if countDL == 3:
                return list(diagL)[0]

        if len(diagR) == 1:
            if countDR == 3:
                return list(diagR)[0]

        if GENCOUNT == (self.size * self.size):
                return "DRAW"

    def doAIMove(self):
        if self.currentTeam == "AI":
            #self.switchTeams()
            pass

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.quitButton.highlighted(mousePos)

        team = self.checkForWin()
        if team:
            self.win(team)

        if self.gameType == BoardWindow.AI:
            self.doAIMove()

    def switchTeams(self):
        if self.currentTeam == "P1":
            self.currentTeam = "P2"
            return

        elif self.currentTeam == "P2":
            self.currentTeam = "P1"
            return

        elif self.currentTeam == "AI":
            self.currentTeam = "PLAYER"
            return

        elif self.currentTeam == "PLAYER":
            self.currentTeam = "AI"
            return

    def event(self, event):
        switch = 0
        endGame = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            for tile in self.tiles.values():
                switch += tile.checkClick(event, self.currentTeam)

            endGame += self.quitButton.checkClick(event)

        if switch > 0:
            self.switchTeams()

        if endGame > 0:
            self.endGame()

class MainMenu:

    def __init__(self, screen) -> None:
        self.screen: Screen = screen
        self.visible = True
        self.createButtons()

    def createButtons(self):

        width = self.screen.width / 6
        height = self.screen.height / 6
        font = pygame.font.SysFont("Comic Sans MS", 30)

        self.AIButton = Button(pygame.Rect(width, height * 2, width, height), "AI", font)
        self.PlayerButton = Button(pygame.Rect(width * 4, height * 2, width, height), "PLAYER", font)

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
        self.boardWindow = BoardWindow(self, self.boardSize, 100)
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