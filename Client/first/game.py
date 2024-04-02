import pygame, sys, socket
from pygame.math import Vector2
from first.player import PLAYER
from first.map import MAP

PROPERTY_DELIMETER = "▐";

# Access command-line arguments
arguments = sys.argv[1:]  # Exclude the first argument, which is the script filename

# Class representing the main game logic
class MAIN:
    def __init__(self, size):
        # Initialize player and map objects
        self.player = PLAYER(int(arguments[0]),int(arguments[1]),int(arguments[2]))
        self.map = MAP(size)
        
    def update(self):
        # Update game state for each frame
        if self.player.alive:
            # Move the player and handle network communication for position updates
            self.player.move()
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
                # Send the player's position to the server
                message = "SAVE_POSITION" + PROPERTY_DELIMETER + str(self.player.id) + PROPERTY_DELIMETER + str(int(self.player.pos.x)) + PROPERTY_DELIMETER + str(int(self.player.pos.y)) + "\n"
                client_socket.sendall(message.encode())
                client_socket.recv(1024)
                client_socket.close()
            except Exception as e:
                print("Save Position error", e)

            self.get_positions()
            try:
                # Check for collisions and update the map accordingly
                self.checkCollision()
                if (self.player.pos.x >= 0 and self.player.pos.x < self.map.size and self.player.pos.y >= 0 and self.player.pos.y < self.map.size):
                    self.map.setValue(int(self.player.pos.x),int(self.player.pos.y),(self.player.id+1))
            except Exception as e:
                print("Main update error:", e)

        else:
            # Handle player removal if not alive
            if not self.player.remove:
                self.remove_by_id(self.player.id)
                self.get_positions()
            self.player.remove = True
            
    def remove_by_id(self, _id):
        # Remove player from the map by setting its position to 0
        for _row in range(cellNumber):
            for _col in range(cellNumber):
                if self.map.getValue(_col, _row) == (_id+1):
                    self.map.setValue(_col, _row, 0)

    def draw(self):
        # Draw player and map on the screen
        self.player.draw(screen, cellSize)
        self.map.drawMap(screen, cellSize)

    def checkCollision(self):
        # Check for collision and set player status
        try:
            if self.player.pos.x < 0 or self.player.pos.x > cellNumber-1 or self.player.pos.y < 0 or self.player.pos.y > cellNumber-1:
                self.player.alive = False
                self.set_dead()
            else:
                if not self.map.getValue(int(self.player.pos.x), int(self.player.pos.y)) == 0:
                    self.player.alive = False
                    self.set_dead()
        except Exception as e:
            print("Collision error:", e)

    def set_dead(self):
        # Notify server that player is dead
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
        # Get positions of all players from the server
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
            message = "GET_POSITIONS\n"
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            client_socket.close()

            # Process the received data
            data_string = data.decode()
            data_string = data_string[:-3]
            data_array = data_string.split(PROPERTY_DELIMETER)
            players = []
            for sub_array in data_array:
                elements = sub_array.split(",")
                elements[1:] = [int(x) for x in elements[1:]]
                players.append(elements)

            # Update the map based on other players' positions
            for _id in range(len(players)):
                if not (_id == self.player.id) and not (_id in dead_list):
                    if players[_id][0] == 'A':
                        back_tail = int((len(players[_id])-1)/2)
                        for _tIndex in range(back_tail):
                            self.map.setValue(players[_id][_tIndex*2+1],players[_id][_tIndex*2+2],_id+1)
                    else:
                        dead_list.append(_id)
                        self.remove_by_id(_id)

            # Check win condition
            if len(dead_list) > len(players) - 2:
                self.player.you_win = True
                        
        except Exception as e:
            print("Connection error update:", e)

    def gameOver(self):
        # Quit the game
        pygame.quit()
        sys.exit()
        

pygame.init()
# Initialize game screen and clock
cellSize = 16
cellNumber = 40 
screen = pygame.display.set_mode((cellSize * cellNumber, cellSize * cellNumber + 50))
clock = pygame.time.Clock()

# Set up networking constants from arguments
SERVER_ADDRESS = arguments[3]
SERVER_PORT = int(arguments[4])

# Initialize game font and colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 36)

# Define a user event for screen updates
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 300)

# Track list of dead players
dead_list = []

# Initialize the main game
mainGame = MAIN(cellNumber)

def draw_text(ip_text, ip_color, x, y):
    # Helper function to draw text on screen
    ip_text_surface = font.render(ip_text, True, ip_color)
    screen.blit(ip_text_surface, (x, y))

while True:
    # Main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            mainGame.update()

        # Handle player movement inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                mainGame.player.direction = Vector2(0,-1) if mainGame.player.direction.y != 1 else Vector2(0,1)
            elif event.key == pygame.K_DOWN:
                mainGame.player.direction = Vector2(0,1) if mainGame.player.direction.y != -1 else Vector2(0,-1)
            elif event.key == pygame.K_LEFT:
                mainGame.player.direction = Vector2(-1,0) if mainGame.player.direction.x != 1 else Vector2(1,0)
            elif event.key == pygame.K_RIGHT:
                mainGame.player.direction = Vector2(1,0) if mainGame.player.direction.x != -1 else Vector2(-1,0)

    # Render the game state
    screen.fill((25,25,25))
    mainGame.draw()
    
    # Display game over or win messages
    if not mainGame.player.alive:
        draw_text("You Lose", WHITE, 200, 200)
    elif mainGame.player.you_win:
        draw_text("You Won", WHITE, 200, 200)
       
    # Draw the HUD
    hud = pygame.Rect(0, cellSize * cellNumber, cellSize * cellNumber, cellSize * cellNumber + 50)
    pygame.draw.rect(screen, (125,125,125), hud)   
    draw_text("you are " + str(mainGame.player.id), mainGame.map.use_color[mainGame.player.id+1], 200, cellSize * cellNumber + 20)
    
    # Refresh the screen
    pygame.display.update()
    clock.tick(60)  # Maintain 60 frames per second
