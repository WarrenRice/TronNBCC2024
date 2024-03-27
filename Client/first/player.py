from pygame.math import Vector2
import pygame

class PLAYER:
    def __init__(self,_id,_posX,_posY):
        #self.bodys = [Vector2(19,38),Vector2(19,39)]
        self.id = _id
        self.pos = Vector2(_posX,_posY)
        self.alive = True
        self.remove = False
        self.you_win = False
        
        if (self.id == 0):
            self.direction = Vector2(1,0)
        elif (self.id == 1):
            self.direction = Vector2(0,-1)
        elif (self.id == 2):
            self.direction = Vector2(0,1)
        elif (self.id == 3):
            self.direction = Vector2(-1,0)    
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