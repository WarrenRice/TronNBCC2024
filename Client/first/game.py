import pygame, sys, socket
from pygame.math import Vector2
from first.player import PLAYER
from first.map import MAP


PROPERTY_DELIMETER = "▐";

# Access arguments
arguments = sys.argv[1:]  # Exclude the first argument, which is the script filename

# Use arguments as needed
# print("Arguments:", arguments)
# print(arguments)

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
            except Exception as e:
                print("Save Position error", e)
                
            self.get_positions()
    
            try:
                self.checkCollision()
                if (self.player.pos.x >= 0 and self.player.pos.x < self.map.size and self.player.pos.y >= 0 and self.player.pos.y < self.map.size):
                    self.map.setValue(int(self.player.pos.x),int(self.player.pos.y),(self.player.id+1))
                    
            except Exception as e:
                print("Main update error:", e)

        else:
            
            if self.player.remove == False:
                
                self.remove_by_id(self.player.id)
                   
                self.get_positions()        

            self.player.remove = True
            
    def remove_by_id(self, _id):
        for _row in range(cellNumber):
            for _col in range(cellNumber):
                if self.map.getValue(_col, _row) == (_id+1) :
                    self.map.setValue(_col,_row,0)

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
    
    def get_positions(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
            message = "GET_POSITIONS\n"
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            client_socket.close()

            data_string = data.decode()
            
            # Remove the last character from the input string
            data_string = data_string[:-3]
            #print("data in: " + str(data_string))
            
            data_array = data_string.split("▐")

            players = []
            
            
            #print("--------------------")
            for sub_array in data_array:
                sub_array = sub_array[:-1]
                #print(sub_array)
                # Split the subarray by "," character
                elements = sub_array.split(",")
                
                # Convert the numeric elements to integers
                elements[1:] = [int(x) for x in elements[1:]]
                #print(elements)
                # Append the modified subarray to the result list
                players.append(elements)
            
            #print(others_players)
            count = 0
            for _id in range(len(players)):
                #print("test")

                if not (_id == self.player.id) and not (_id in dead_list):
                    #print("players[_index]")
                    #print(players[_id])
                    #print(int(len(players[_index])-1)/2)
                    if (players[_id][0] == 'A'):
                        back_tail = int((len(players[_id])-1)/2)
                        for _tIndex in range(back_tail):
                            self.map.setValue(players[_id][_tIndex*2+1],players[_id][_tIndex*2+2],_id+1)
                    else:
                        dead_list.append(_id)
                        self.remove_by_id(_id)


            if (len(dead_list) > len(players)-2):
                self.player.you_win = True
            
                        
        except Exception as e:
            print("Connection error update:", e)
    def gameOver(self):
        pygame.quit()
        sys.exit()
        

pygame.init()
cellSize = 16
cellNumber = 40 
screen = pygame.display.set_mode((cellSize *cellNumber,cellSize *cellNumber + 50))
clock = pygame.time.Clock()

# Set up networking
SERVER_ADDRESS = arguments[3]  # Change this to your server's IP address
SERVER_PORT = int(arguments[4])

# Font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 36)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,300)

dead_list = []

mainGame = MAIN(cellNumber)

def draw_text(ip_text, ip_color, x, y):
    ip_text_surface = font.render(ip_text, True, ip_color)
    screen.blit(ip_text_surface, (x, y))

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
    
    # Check if player is alive
    if not mainGame.player.alive:
        draw_text("You Lose", WHITE, 200, 200)  # Display "You Lose" text
    elif mainGame.player.you_win:
        draw_text("You Won", WHITE, 200, 200)
       
    hud = pygame.Rect(0,cellSize *cellNumber,cellSize *cellNumber,cellSize *cellNumber+50)
    pygame.draw.rect(screen, (125,125,125), hud)   
    draw_text("you are " + str(mainGame.player.id), mainGame.map.use_color[mainGame.player.id+1], 200, cellSize *cellNumber+20)
    
    
    pygame.display.update()
    clock.tick(60) #60 frame/second add comments properly