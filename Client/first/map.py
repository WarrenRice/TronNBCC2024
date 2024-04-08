import pygame
#from first.gameColor import COLORS
# try and catch 
try: 
    from first.gameColor import COLORS 
except Exception as e:
    print(e)
    
    
try: 
    from gameColor import COLORS
except Exception as e:
    print(e)


class MAP:
    def __init__(self, size):
        # Initialize the map with the specified size and set all cells to 0
        self.size = size
        self.map = [[0] * size for _ in range(size)]  # Create a square grid
        self.use_color = COLORS()  # Initialize the COLOR class to use for cell coloring

    def setValue(self, x, y, value):
        # Set the value of a cell in the map at the specified (x, y) coordinates
        if 0 <= x < self.size and 0 <= y < self.size:
            self.map[x][y] = value
        else:
            raise IndexError("Coordinates out of bounds")  # Error if coordinates are invalid

    def getValue(self, x, y):
        # Get the value of a cell in the map at the specified (x, y) coordinates
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.map[x][y]
        else:
            raise IndexError("Coordinates out of bounds")  # Error if coordinates are invalid

    def printMap(self):
        # Print the map to the console (for debugging or text-based output)
        for row in range(self.size):
            line = ""
            for col in range(self.size):
                line += " " + str(self.map[col][row])
            print(line)

    def drawMap(self, screen, cellSize):
        # Draw the map onto the given Pygame screen with each cell of the specified cellSize
        for row in range(self.size):
            for col in range(self.size):
                xPos = int(col * cellSize)  # Calculate the x position on the screen
                yPos = int(row * cellSize)  # Calculate the y position on the screen
                bodyRect = pygame.Rect(xPos, yPos, cellSize, cellSize)
                # Draw the rectangle for the map cell
                pygame.draw.rect(screen, self.use_color[self.map[col][row]], bodyRect)

                '''
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

                    pygame.draw.rect(screen,(75,75,255), bodyRect)
                elif self.map[col][row] == 4:
                    xPos = int(col*cellSize)
                    yPos = int(row*cellSize)
                    bodyRect = pygame.Rect(xPos,yPos,cellSize,cellSize)

                    pygame.draw.rect(screen,(255,255,0), bodyRect)
                '''