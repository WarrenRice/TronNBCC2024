import pygame, sys, socket
from pygame.math import Vector2
#from first.player import PLAYER
#from first.map import MAP

try: 
    from first.player import PLAYER
    from first.map import MAP
except Exception as e:
    from player import PLAYER
    from map import MAP


# rounded corner
# disconnect methods in lobby
# add maps
# players die when disconnect
# make lose become spectator

# Constants and global variables

PROPERTY_DELIMETER = "▐";

# Access arguments
arguments = sys.argv[1:]  # Exclude the first argument, which is the script filename

# Use arguments as needed
# print("Arguments:", arguments[5])
# print(arguments)
# MAIN class manages the game state, including players and the map

class MAIN:
    def __init__(self, size):
        self.player = PLAYER(int(arguments[0]),int(arguments[1]),int(arguments[2]),arguments[5])
        self.map = MAP(size)
        self.load_map("maps/map2.txt")
    # Load map data from a specified file and set map values accordingly

    def load_map(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read().strip()  # Read the content and remove leading/trailing whitespace
                
                if not content:
                    print("File is empty.")
                    return None
                
                data = content.split('|')  # Split the content by '|' to get individual coordinates
                coordinates = [tuple(map(int, coord.split(','))) for coord in data]  # Convert each coordinate string to a tuple of integers
            #print("Coordinates loaded successfully:", coordinates)
            for _ in range(len(coordinates)):
                #print(coordinates[_][0])
                self.map.setValue(coordinates[_][0], coordinates[_][1], 5)
            return coordinates
        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as e:
            print("An error occurred:", e)
            return None
    
    def update(self):    # Main game update loop: handles player movement, collisions, and networking


        if self.player.alive:
            if not self.player.you_win:  # Handle player movement and interactions

                
    
                try:# to save player position
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
                    
                self.player.move() #update position
            else:
                self.get_positions()

        else:
            if self.player.remove == False:
                
                self.remove_by_id(self.player.id)
                
                self.get_positions()

                self.player.remove = True
                
            else:
                self.get_positions()
            
    def remove_by_id(self, _id): # Remove player's presence from the map based on their ID

        for _row in range(cellNumber):
            for _col in range(cellNumber):
                if self.map.getValue(_col, _row) == (_id+1) :
                    self.map.setValue(_col,_row,0)

    def draw(self):    # Draw game elements on the screen

        self.player.draw(screen,cellSize)
        self.map.drawMap(screen,cellSize)

    def checkCollision(self):    # Check for collisions and update player status


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

    def set_dead(self):    # Handle player death in the game

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

            message = "DIE" + PROPERTY_DELIMETER + str(self.player.id) + "\n"
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            
            #print(data.decode())
        
            client_socket.close()
        
        except Exception as e:
            print("Connection error:", e)     
    
    def get_positions(self):    # Retrieve and process the positions of all players from the server

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
            # print(list(data_array))
            for sub_array in data_array:
                if (sub_array == 'IGNORE'):
                    # players.append(sub_array)
                    continue
                
                sub_array = sub_array[:-1]
                #print(sub_array)
                # Split the subarray by "," character
                elements = sub_array.split(",")
                
                # Convert the numeric elements to integers
                elements[2:] = [int(x) for x in elements[2:]]
                #print(elements)
                # Append the modified subarray to the result list
                players.append(elements)
            #print(others_players)
            for idx in range(len(players)):
                #print("test")
                if (players[idx] == 'IGNORE'):
                    continue
                _id = int(players[idx][0])
                if not (_id == self.player.id) and not (_id in dead_list):
                #if not (_id in dead_list):
                    # print("players[_index]")
                    # print(players[_id])
                    # print(int(len(players[idx])-1)/2)
                    if (players[idx][1] == 'A'):
                        back_tail = int((len(players[idx])-1)/2)
                        for _tIndex in range(back_tail):
                            self.map.setValue(players[idx][_tIndex*2+2],players[idx][_tIndex*2+3],_id+1)
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
        
# Initialize Pygame and set up the display

pygame.init()
cellSize = 8#16
cellNumber = 100#40 
screen = pygame.display.set_mode((cellSize *cellNumber,cellSize *cellNumber + 50))
clock = pygame.time.Clock()

# Networking setup

SERVER_ADDRESS = arguments[3]  # Change this to your server's IP address
SERVER_PORT = int(arguments[4])

# Font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Set up the event for screen update

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,300)

# List to keep track of dead players
dead_list = []

# Create the main game object
mainGame = MAIN(cellNumber)
# Function to draw text on the screen

def draw_text(text, color, x, y, size=36):  # Default font size is 36
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to draw rounded rectangles (used for pop-up messages, etc.)

def draw_rounded_rectangle(surface, color, rect, radius=20):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    
# Main game loop: handles events, updates game state, and draws game elements

def show_popup_message(message):
    popup_screen = pygame.display.set_mode((300, 200))  # Define pop-up window size
    popup_screen.fill((255, 255, 255))  # Fill pop-up window with white background

    font = pygame.font.Font(None, 36)  # Set font and size for the message
    text_surface = font.render(message, True, (0, 0, 0))  # Render the message

    # Calculate position to center the message on the pop-up window
    text_rect = text_surface.get_rect(center=(150, 100))

    popup_screen.blit(text_surface, text_rect)  # Draw the message on the pop-up window

    pygame.display.flip()  # Update the pop-up window display

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

while True:
    #draw all elements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainGame.player.alive = False
            mainGame.set_dead()
            #print(mainGame.player.alive)
            #mainGame.printStm()
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            mainGame.update()

        if event.type == pygame.KEYDOWN:# movement (w,a,s,d)to move the player
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if mainGame.player.direction.y != 1:
                    mainGame.player.direction = Vector2(0,-1)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if mainGame.player.direction.y != -1:
                    mainGame.player.direction = Vector2(0,1)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if mainGame.player.direction.x != 1:
                    mainGame.player.direction = Vector2(-1,0)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if mainGame.player.direction.x != -1:
                    mainGame.player.direction = Vector2(1,0)

    screen.fill((25,25,25))
    mainGame.draw()
    
    # Check if player is alive
    if not mainGame.player.alive:
        rounded_rect = pygame.Rect(cellSize *cellNumber/2-125, cellSize *cellNumber/2-50, 250, 100)
        draw_rounded_rectangle(screen, (255, 255, 255, 128), rounded_rect)  # 50% transparent black
        draw_text("You Lose", BLACK, cellSize *cellNumber/2-110, cellSize *cellNumber/2-20, size=72)  # Display "You Lose" text
        #show_popup_message("You Lose")  # Display pop-up window with "You Lose" message
    
    elif mainGame.player.you_win:
        rounded_rect = pygame.Rect(cellSize *cellNumber/2-125, cellSize *cellNumber/2-50, 250, 100)
        draw_rounded_rectangle(screen, (255, 255, 255, 128), rounded_rect)  # 50% transparent black
        draw_text("You Won", BLACK, cellSize *cellNumber/2-105, cellSize *cellNumber/2-25, size=72)
        #show_popup_message("You Won")  # Display pop-up window with "You Won" message
        
    hud = pygame.Rect(0,cellSize *cellNumber,cellSize *cellNumber,cellSize *cellNumber+50)
    pygame.draw.rect(screen, (125,125,125), hud)   
    draw_text(mainGame.player.name + " are player " + str(mainGame.player.id + 1), mainGame.map.use_color[mainGame.player.id+1], 20, cellSize *cellNumber+12)
    draw_text("(Press Arrow Keys or 'W','A','S','D' to move)", mainGame.map.use_color[mainGame.player.id+1], 250, cellSize *cellNumber+12)
    #draw_text("Note: press Arrow Keys or 'W','A','S','D' to move", 200, cellSize *cellNumber+12)
    
    pygame.display.update()
    clock.tick(60) #60 frame/second add comments properly