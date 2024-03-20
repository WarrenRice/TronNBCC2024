import pygame, sys, random, socket
from pygame.math import Vector2

class PLAYER:
    def __init__(self):
        #self.bodys = [Vector2(19,38),Vector2(19,39)]
        self.pos = Vector2(19,39)
        self.direction = Vector2(0,-1)

    def draw(self):
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

    def drawMap(self):
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

class MAIN:

    def __init__(self, size):
        self.player = PLAYER()
        self.map = MAP(size)
    
    def update(self):
        self.player.move()
        self.checkCollision()
        self.map.setValue(int(self.player.pos.x),int(self.player.pos.y),1)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

        #message = "Player position: {},{}".format(int(mainGame.player.pos.x), int(mainGame.player.pos.y))
        message = "CONNECT\n"
        client_socket.sendall(message.encode())
        
        data = client_socket.recv(1024)
        print(data.decode())
        
        client_socket.close()

        self.map.setValue(19,0,2)
        self.map.setValue(19,1,2)
        self.map.setValue(19,2,2)
        self.map.setValue(19,3,2)
        self.map.setValue(20,3,2)
        self.map.setValue(21,3,2)
        self.map.setValue(22,3,2)
        self.map.setValue(22,4,2)
        self.map.setValue(22,5,2)
        self.map.setValue(22,6,2)
        self.map.setValue(22,7,2)
        self.map.setValue(23,7,2)
        self.map.setValue(24,7,2)


        self.map.setValue(39,19,3)
        self.map.setValue(38,19,3)
        self.map.setValue(37,19,3)
        self.map.setValue(36,19,3)
        self.map.setValue(35,19,3)
        self.map.setValue(35,20,3)
        self.map.setValue(35,21,3)
        self.map.setValue(35,22,3)
        self.map.setValue(35,23,3)
        self.map.setValue(35,24,3)
        self.map.setValue(35,25,3)
        self.map.setValue(35,26,3)


        self.map.setValue(0,19,4)
        self.map.setValue(1,19,4)
        self.map.setValue(2,19,4)
        self.map.setValue(3,19,4)
        self.map.setValue(4,19,4)
        self.map.setValue(5,19,4)
        self.map.setValue(6,19,4)
        self.map.setValue(7,19,4)
        self.map.setValue(8,19,4)
        self.map.setValue(8,18,4)
        self.map.setValue(8,17,4)
        self.map.setValue(8,16,4)
        self.map.setValue(9,16,4)

        

        #self.map.printMap()

    def draw(self):
        self.player.draw()
        self.map.drawMap()

    def checkCollision(self):

        if not 0 <= self.player.pos.x <= cellNumber or not 0 <= self.player.pos.y <= cellNumber :
            self.gameOver()
        
        '''
        for block in self.player.bodys[1:]:
            if block == self.player.bodys[0]:
                #self.gameOver()
                pass
        '''

        if not self.map.getValue(int(self.player.pos.x),int(self.player.pos.y)) == 0:
            self.gameOver()


        
    def gameOver(self):
        pygame.quit()
        sys.exit()
        

pygame.init()
cellSize = 16
cellNumber = 40 
screen = pygame.display.set_mode((cellSize *cellNumber,cellSize *cellNumber))
clock = pygame.time.Clock()

# Set up networking
SERVER_ADDRESS = '127.0.0.1'  # Change this to your server's IP address
SERVER_PORT = 6066



SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

mainGame = MAIN(cellNumber)

while True:
    #draw all elements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            mainGame.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if mainGame.player.direction.y != 1:
                    mainGame.player.direction = Vector2(0,-1)
            elif event.key == pygame.K_DOWN:
                if mainGame.player.direction.y != -1:
                    mainGame.player.direction = Vector2(0,1)
            elif event.key == pygame.K_LEFT:
                if mainGame.player.direction.x != 1:
                    mainGame.player.direction = Vector2(-1,0)
            elif event.key == pygame.K_RIGHT:
                if mainGame.player.direction.x != -1:
                    mainGame.player.direction = Vector2(1,0)

    screen.fill((25,25,25))
    mainGame.draw()
    pygame.display.update()
    clock.tick(60) #60 frame/second