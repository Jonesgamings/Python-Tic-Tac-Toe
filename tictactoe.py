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
    
    def __init__(self, screen, size) -> None:
        self.screen = screen
        self.visible = False
        self.size = size

class MainMenu:

    def __init__(self, screen) -> None:
        self.screen = screen
        self.visible = False

class Screen:

    def __init__(self, width, height) -> None:
        self.boardSize = 3
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        self.boardWindow = BoardWindow(self, self.boardSize)
        self.mainmanu = MainMenu(self)