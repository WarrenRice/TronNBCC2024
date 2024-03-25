import pygame, sys, random, socket
from pygame.math import Vector2
from first.player import PLAYER
from first.map import MAP


PROPERTY_DELIMETER = "▐";

# Access arguments
arguments = sys.argv[1:]  # Exclude the first argument, which is the script filename

# Use arguments as needed
#print("Arguments:", arguments)


class MAIN:
    def __init__(self, size):
        self.player = PLAYER(int(arguments[0]),int(arguments[1]),int(arguments[2]))
        self.map = MAP(size)
        
    def update(self):
        if self.player.alive:
            self.player.move() #update position
            
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
                message = "SAVE_POSITION" + PROPERTY_DELIMETER + str(self.player.id) + PROPERTY_DELIMETER + str(int(self.player.pos.x)) + PROPERTY_DELIMETER + str(int(self.player.pos.y)) + "\n"
                client_socket.sendall(message.encode())
                client_socket.recv(1024)
                client_socket.close()
                
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
                message = "GET_POSITIONS\n"
                client_socket.sendall(message.encode())
                data = client_socket.recv(1024)
                client_socket.close()

                data_string = data.decode()
                
                # Remove the last character from the input string
                data_string = data_string[:-3]

                data_array = data_string.split("▐")
                
                print("data in: " + str(data_string))
                print("data in: " + str(len(data_array)))
                
                
                
                
            except Exception as e:
                print("Connection error:", e)
    
            try:
                self.checkCollision()
                if (self.player.pos.x >= 0 and self.player.pos.x < self.map.size and self.player.pos.y >= 0 and self.player.pos.y < self.map.size):
                    self.map.setValue(int(self.player.pos.x),int(self.player.pos.y),(self.player.id+1))
                    
            except Exception as e:
                print("Main update error:", e)
    
            
    
            '''
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
            '''
            
        else:
            pass
            #self.map.printMap()

    def draw(self):
        self.player.draw(screen,cellSize)
        self.map.drawMap(screen,cellSize)

    def checkCollision(self):

        try:
            if self.player.pos.x < 0 or self.player.pos.x > cellNumber-1 or self.player.pos.y < 0 or self.player.pos.y > cellNumber-1:
                #if (self.player.alive):
                self.player.alive = False
                self.set_dead()
            
            
            
            #if not (0 <= self.player.pos.x <= cellNumber) or not (0 <= self.player.pos.y <= cellNumber) :
                
            else:
                if not self.map.getValue(int(self.player.pos.x),int(self.player.pos.y)) == 0:
                    #if (self.player.alive):
                    self.player.alive = False
                    self.set_dead()
                    
            '''
            for block in self.player.bodys[1:]:
                if block == self.player.bodys[0]:
                    #self.gameOver()
                    pass
            '''
        except Exception as e:
            print("Collision error:", e)

    def set_dead(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

            message = "DIE" + PROPERTY_DELIMETER + str(self.player.id) + "\n"
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            
            print(data.decode())
        
            client_socket.close()
        
        except Exception as e:
            print("Connection error:", e)     
    
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