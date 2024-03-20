from pygame.math import Vector2
import pygame

class PLAYER:
    def __init__(self,id,posX,posY):
        #self.bodys = [Vector2(19,38),Vector2(19,39)]
        self.id = id
        self.pos = Vector2(posX,posY)
        self.direction = Vector2(0,-1)
        
        #self.pos = Vector2(-1,-1)
        #self.direction = Vector2(0,0)

    def draw(self, screen, cellSize):
        xPos = int(self.pos.x*cellSize)
        yPos = int(self.pos.y*cellSize)
        bodyRect = pygame.Rect(xPos,yPos,cellSize,cellSize)
        pygame.draw.rect(screen,(255,0,0), bodyRect)

        '''
        for body in self.bodys:
            xPos = int(body.x*cellSize)
            yPos = int(body.y*cellSize)
            bodyRect = pygame.Rect(xPos,yPos,cellSize,cellSize)

            pygame.draw.rect(screen,(255,0,0), bodyRect)
        '''
        
    def move(self):
        #bodysCopy = self.bodys[:]
        #bodysCopy.insert(0,bodysCopy[0] + self.direction)
        #self.bodys = bodysCopy[:]
        self.pos = self.pos + self.direction