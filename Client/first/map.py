import pygame

class MAP:
    def __init__(self, size):
        self.size = size
        self.map = [[0] * size for _ in range(size)]

    def setValue(self, x, y, value):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.map[x][y] = value
        else:
            raise IndexError("Coordinates out of bounds")

    def getValue(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.map[x][y]
        else:
            raise IndexError("Coordinates out of bounds")

    def printMap(self):
        for row in range(self.size):
            line = ""
            for col in range(self.size):
                line = line + " " + str(self.map[col][row])
            print(line)

    def drawMap(self, screen, cellSize):
        for row in range(self.size):
            for col in range(self.size):
                if self.map[col][row] == 1:
                    xPos = int(col*cellSize)
                    yPos = int(row*cellSize)
                    bodyRect = pygame.Rect(xPos,yPos,cellSize,cellSize)

                    pygame.draw.rect(screen,(255,0,0), bodyRect)
                elif self.map[col][row] == 2:
                    xPos = int(col*cellSize)
                    yPos = int(row*cellSize)
                    bodyRect = pygame.Rect(xPos,yPos,cellSize,cellSize)

                    pygame.draw.rect(screen,(0,255,0), bodyRect)
                elif self.map[col][row] == 3:
                    xPos = int(col*cellSize)
                    yPos = int(row*cellSize)
                    bodyRect = pygame.Rect(xPos,yPos,cellSize,cellSize)

                    pygame.draw.rect(screen,(0,0,255), bodyRect)
                elif self.map[col][row] == 4:
                    xPos = int(col*cellSize)
                    yPos = int(row*cellSize)
                    bodyRect = pygame.Rect(xPos,yPos,cellSize,cellSize)

                    pygame.draw.rect(screen,(0,255,255), bodyRect)