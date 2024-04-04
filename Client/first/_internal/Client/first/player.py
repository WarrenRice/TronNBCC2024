from pygame.math import Vector2
import pygame

class PLAYER:
    def __init__(self, _id, _posX, _posY):
        # Initialize the player with an ID, position, and alive status
        self.id = _id  # Unique identifier for the player
        self.pos = Vector2(_posX, _posY)  # Current position of the player
        self.alive = True  # Status to track if the player is alive
        self.remove = False  # Flag to check if the player needs to be removed
        self.you_win = False  # Status to check if the player has won
        
        # Set the initial direction of movement based on the player's ID
        if self.id == 0:
            self.direction = Vector2(1, 0)  # Right
        elif self.id == 1:
            self.direction = Vector2(0, -1)  # Up
        elif self.id == 2:
            self.direction = Vector2(0, 1)  # Down
        elif self.id == 3:
            self.direction = Vector2(-1, 0)  # Left

    def draw(self, screen, cellSize):
        # Draw the player on the screen as a rectangle
        xPos = int(self.pos.x * cellSize)  # Calculate the x position on the screen
        yPos = int(self.pos.y * cellSize)  # Calculate the y position on the screen
        bodyRect = pygame.Rect(xPos, yPos, cellSize, cellSize)  # Define the player's rectangle
        pygame.draw.rect(screen, (255, 0, 0), bodyRect)  # Draw the player's rectangle

    def move(self):
        # Update the player's position based on the current direction
        self.pos = self.pos + self.direction  # Move the player in the direction they are facing
