import pygame, sys, socket
from pygame.math import Vector2
#from first.player import PLAYER
#from first.map import MAP

try: 
    from first.player import PLAYER
    from first.map import MAP
except Exception as e:
    pass


try: 
    from player import PLAYER
    from map import MAP
except Exception as e:
    pass

<<<<<<< HEAD
# Constants and global variables
=======


>>>>>>> 3b1c40b5a8ed7e897e7df74ad175928cd7864399

PROPERTY_DELIMETER = "▐";                                                                       # Define a delimiter for parsing server messages

arguments = sys.argv[1:]                                                                         # Exclude the first argument, which is the script filename

# Use arguments as needed
# print("Arguments:", arguments[5])
# print(arguments)
# MAIN class manages the game state, including players and the map
class MAIN:
    def __init__(self, size):                                                                   # Initialize the MAIN class with a map size and player setup


        self.player = PLAYER(int(arguments[0]),int(arguments[1]),int(arguments[2]),arguments[5])
        self.map = MAP(size)
<<<<<<< HEAD
        self.load_map("maps/map2.txt")# Load the map from a specified file
=======
        self.load_map("maps/map2.txt")                                                          # Load the map from a specified file
    # Load map data from a specified file and set map values accordingly
>>>>>>> 3b1c40b5a8ed7e897e7df74ad175928cd7864399

    # Load map data from a specified file and set map values accordingly
    def load_map(self, file_path):
        try:                                                                                    # Load map data from a text file and set map values
            with open(file_path, 'r') as file:                                                  # Open the file for reading
                content = file.read().strip()                                                   # Read the content and remove leading/trailing whitespace
                
                if not content:                                                                 # Check if the file is empty
                    print("File is empty.")
                    return None
                
                data = content.split('|')                                                       # Split the content by '|' to get individual coordinates
                coordinates = [tuple(map(int, coord.split(','))) for coord in data]             # Convert each coordinate string to a tuple of integers
            #print("Coordinates loaded successfully:", coordinates)
            for _ in range(len(coordinates)):                                                   # Set values in the map for each coordinate
                #print(coordinates[_][0])
                self.map.setValue(coordinates[_][0], coordinates[_][1], 5)
            return coordinates
        except FileNotFoundError:                                                                # Handle file not found error
            print("File not found.")
            return None
        except Exception as e:
            print("An error occurred:", e)                                                       # Handle any other exceptions
            return None
    
    def update(self):                                                                            # Main game update loop: handles player movement, collisions, and networking


        if self.player.alive:                                                                    # Update game state, handling player movement, collisions, and networking
            if not self.player.you_win:                                                          # Handle player movement and interactions

<<<<<<< HEAD
                try:# Establish a network connection to save player position
=======
                
    
                try:                                                                             # Establish a network connection to save player position
>>>>>>> 3b1c40b5a8ed7e897e7df74ad175928cd7864399
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
                    message = "SAVE_POSITION" + PROPERTY_DELIMETER + str(self.player.id) + PROPERTY_DELIMETER + str(int(self.player.pos.x)) + PROPERTY_DELIMETER + str(int(self.player.pos.y)) + "\n"
                    client_socket.sendall(message.encode())                                      # Send the position data to the server
                    client_socket.recv(1024)                                                     # Receive acknowledgment from the server
                    client_socket.close()                                                        # Close the socket connection
                except Exception as e:
                    print("Save Position error", e)                                              # Print error if position saving fails
                    
                self.get_positions()                                                             # Retrieve player positions from the server
        
                try:
                    self.checkCollision()                                                                                                              # Check for collisions with map boundaries or other entities
                    if (self.player.pos.x >= 0 and self.player.pos.x < self.map.size and self.player.pos.y >= 0 and self.player.pos.y < self.map.size):
                        self.map.setValue(int(self.player.pos.x),int(self.player.pos.y),(self.player.id+1))                                            # Update map with player's new position
                        
                except Exception as e:
                    print("Main update error:", e)                                                # Print error if main update fails
                    
                self.player.move()                                                                # Move the player based on current direction and speed
            else:
                self.get_positions()                                                              # Retrieve player positions from the server if player has won


        else:
            if self.player.remove == False:                                                       # Check if the player has already been removed from the game
                
                self.remove_by_id(self.player.id)                                                 # Remove player's presence from the map
                
                self.get_positions()                                                              # Update positions after removing the player

                self.player.remove = True                                                         # Mark the player as removed
                
            else:
                self.get_positions()                                                              # Update positions if the player is already removed
            
            
    def remove_by_id(self, _id):                                                                  # Remove a player's presence from the map using their ID

        for _row in range(cellNumber):                                                            # Iterate through map rows
            for _col in range(cellNumber):                                                        # Iterate through map col
                if self.map.getValue(_col, _row) == (_id+1) :                                     # Check if the tile belongs to the player
                    self.map.setValue(_col,_row,0)                                                # Set the tile value to 0, removing the player's presence


    def draw(self):                                                                               # Draw game elements on the screen

        self.player.draw(screen,cellSize)                                                         # Draw the player
        self.map.drawMap(screen,cellSize)                                                         # Draw the map

    def checkCollision(self):                                                                     # Check for collisions and update player status
        
        try:                                                                                      # Check for collisions with map boundaries or other obstacles
            if self.player.pos.x < 0 or self.player.pos.x > cellNumber-1 or self.player.pos.y < 0 or self.player.pos.y > cellNumber-1:            # Check if player is outside map boundaries and set player as not alive if so

                #if (self.player.alive):
                self.player.alive = False
                self.set_dead()

            #if not (0 <= self.player.pos.x <= cellNumber) or not (0 <= self.player.pos.y <= cellNumber) :
                
            else:                # Check if the player's current position on the map is not empty (collision with an obstacle)

                if not self.map.getValue(int(self.player.pos.x),int(self.player.pos.y)) == 0:
                    #if (self.player.alive):
                    self.player.alive = False
                    self.set_dead()
                    
        except Exception as e:
            print("Collision error:", e)                                                          # Print error if collision checking fails


    def set_dead(self):                                                                            # Communicate to the server that the player has died


        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                      # Create a socket object
            client_socket.connect((SERVER_ADDRESS, SERVER_PORT))                                   # Connect to the server

            message = "DIE" + PROPERTY_DELIMETER + str(self.player.id) + "\n"                      # Prepare the death message

            client_socket.sendall(message.encode())                                                # Send the death message to the server
            data = client_socket.recv(1024)                                                        # Receive acknowledgment from the server
            
            #print(data.decode())
        
            client_socket.close()                                                                  # Close the socket connection
        
        except Exception as e:
            print("Connection error:", e)     
    
    def get_positions(self):                                                                       # Retrieve and process the positions of all players from the server

        try:                                                                                       # Get the current positions of all players from the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                      # Create a socket object
            client_socket.connect((SERVER_ADDRESS, SERVER_PORT))                                   # Connect to the server
            message = "GET_POSITIONS\n"                                                            # Prepare the position message
            client_socket.sendall(message.encode())                                                # Send the position message to the server
            data = client_socket.recv(1024)                                                        # Receive acknowledgment from the server
            client_socket.close()                                                                  # Close the socket connection

            data_string = data.decode()                                                            # Decode and strip the trailing characters from the data string
            
            # Remove the last character from the input string
            data_string = data_string[:-3]                                                         # Split the data string into an array using the delimiter
            #print("data in: " + str(data_string))
            
            data_array = data_string.split("▐")

            players = []                                                                            # Initialize an empty list to hold player data

            
            
            #print("--------------------")
            # print(list(data_array))
            for sub_array in data_array:
                if (sub_array == 'IGNORE'):                                                           # Skip entries marked as 'IGNORE'
                    # players.append(sub_array)
                    continue
                
                sub_array = sub_array[:-1]                                                             # Remove the trailing comma from the subarray
                #print(sub_array)
                elements = sub_array.split(",")                                                        # Split the subarray into elements
                
                
                elements[2:] = [int(x) for x in elements[2:]]                                          # Convert string numbers to integers
                #print(elements)
                # Append the modified subarray to the result list
                players.append(elements)                                                               # Add the processed player data to the list

            #print(others_players)
            for idx in range(len(players)):
                #print("test")
                if (players[idx] == 'IGNORE'):
                    continue
                _id = int(players[idx][0])                                                              # Get the player ID from the data
                if not (_id == self.player.id) and not (_id in dead_list):                              # Check if the player is not the current player and not already in the dead list
                #if not (_id in dead_list):
                    # print("players[_index]")
                    # print(players[_id])
                    # print(int(len(players[idx])-1)/2)
                    if (players[idx][1] == 'A'):                                                         # Check if the player is alive
                        back_tail = int((len(players[idx])-1)/2)                                         # Calculate the number of position elements
                        for _tIndex in range(back_tail):                                                 # Iterate through the position elements
                            self.map.setValue(players[idx][_tIndex*2+2],players[idx][_tIndex*2+3],_id+1) # Update the map with the player's positions
                    else:
                        dead_list.append(_id)                                                           # Add the player to the dead list
                        self.remove_by_id(_id)                                                          # Remove the player from the map
            
            if (len(dead_list) > len(players)-2):                                                       # Check if the current player is the last one alive
                self.player.you_win = True                                                              # Set the player's win status to true
            
                        
        except Exception as e:
            print("Connection error update:", e)                                                        # Print error if there is a connection issue during position update
            
    def game_over(self):                                                                                # Quit the game and close the application

        
        pygame.quit()
        sys.exit()
        
         
    def reset_server(self):                                                                              # Send a request to the server to reset the game state

        try:
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                            # Create a socket object
            
            client_socket.connect((SERVER_ADDRESS, SERVER_PORT))                                         # Connect to the server

            text = "RESET\n"                                                                             # Prepare the reset message
            client_socket.sendall(text.encode())
            
            client_socket.close()
    
        except Exception as e:
            print("reset_server error:", e)    

# Initialize Pygame and set up the display

pygame.init()                                                                                             # Initialize all imported Pygame modules
cellSize = 8                                                                                              #16 # Define the size of each cell on the grid
cellNumber = 100                                                                                          #40 # Define the number of cells in the grid
screen = pygame.display.set_mode((cellSize *cellNumber,cellSize *cellNumber + 50))                        # Set up the display window
clock = pygame.time.Clock()                                                                               # Create a clock object to manage updates

# Networking setup

SERVER_ADDRESS = arguments[3]                                                                             # Server IP address from command line argument
SERVER_PORT = int(arguments[4])                                                                           # Server port from command line arguments

# Font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


exit_button_rect = pygame.Rect(cellSize *cellNumber/2-100, cellSize *cellNumber/2 + 80, 200, 50)           # Setup a rectangle for the exit button
exit_button_color = (0,255,0)
exit_button_text = "Exit"
exit_button_text_color = BLACK


SCREEN_UPDATE = pygame.USEREVENT                                                                           # Set up the event for screen update 
pygame.time.set_timer(SCREEN_UPDATE,300)                                                                   # Trigger SCREEN_UPDATE event every 300 milliseconds

dead_list = []                                                                                             # List to keep track of dead players



mainGame = MAIN(cellNumber)                                                                                # Create the main game object


def draw_text(text, color, x, y, size=36):                                                                 #  Function to draw text on the screen

    font = pygame.font.Font(None, size)                                                                   

    text_surface = font.render(text, True, color)                                                          
    screen.blit(text_surface, (x, y))                                                                      

def draw_rounded_rect(surface, color, rect, radius=10):                                                    # Function to draw rounded rectangles (used for pop-up messages, etc.)

    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_button_with_rounded_corners(text, rect, color, text_color, offsetX, radius=10):                     # Function to draw a button with rounded corners and text

    draw_rounded_rect(screen, color, rect, radius)
    draw_text(text, text_color, rect.x + offsetX, rect.y + 12)
    

def show_popup_message(message):                                                                              # Function to show a popup message

    popup_screen = pygame.display.set_mode((300, 200))                                                        # Define pop-up window size
    popup_screen.fill((255, 255, 255))                                                                        # Fill pop-up window with white background

    font = pygame.font.Font(None, 36)                                                                         # Set font and size for the message
    text_surface = font.render(message, True, (0, 0, 0))                                                      # Render the message

    text_rect = text_surface.get_rect(center=(150, 100))                                                      # Calculate position to center the message on the pop-up window


    popup_screen.blit(text_surface, text_rect)                                                                # Draw the message on the pop-up window

    pygame.display.flip()                                                                                     # Update the pop-up window display

    while True:                                                                                               # Wait for an event to close the popup
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

while True:                                                                                                   # Main game loop

    # Process events and update game state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                                                         # Handle window close event

            mainGame.player.alive = False
            mainGame.set_dead()
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:                                                                       # Update game state on screen refresh event

            mainGame.update()

        if event.type == pygame.KEYDOWN:                                                                     # movement (w,a,s,d)to move the player
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
        
        if event.type == pygame.MOUSEBUTTONDOWN and (not mainGame.player.alive or mainGame.player.you_win):   # Handle mouse click on the exit button when the player is dead or has won

            if exit_button_rect.collidepoint(event.pos):
                mainGame.game_over()
                
                
    screen.fill((25,25,25))                                                                                    # Fill the screen with a dark background
    mainGame.draw()                                                                                            # Draw the game elements
    
    # Display game over or win messages and buttons

    if not mainGame.player.alive or mainGame.player.you_win:
        if not mainGame.player.alive:
            rounded_rect = pygame.Rect(cellSize *cellNumber/2-125, cellSize *cellNumber/2-50, 250, 100)
            draw_rounded_rect(screen, (255, 255, 255), rounded_rect)                                           # 50% transparent black
            draw_text("You Lose", BLACK, cellSize *cellNumber/2-110, cellSize *cellNumber/2-20, size=72)       # Display "You Lose" text
            #show_popup_message("You Lose")  # Display pop-up window with "You Lose" message
            
        else:
            rounded_rect = pygame.Rect(cellSize *cellNumber/2-125, cellSize *cellNumber/2-50, 250, 100)
            draw_rounded_rect(screen, (255, 255, 255), rounded_rect)                                          # 50% transparent black
            draw_text("You Won", BLACK, cellSize *cellNumber/2-105, cellSize *cellNumber/2-25, size=72)
            #show_popup_message("You Won")  # Display pop-up window with "You Won" message
            mainGame.reset_server()
        
        draw_rounded_rect(screen, exit_button_color, exit_button_rect)
        draw_text("Exit", BLACK, cellSize *cellNumber/2-35, cellSize *cellNumber/2+90, size=48)
            
    #elif mainGame.player.you_win:

        
    hud = pygame.Rect(0,cellSize *cellNumber,cellSize *cellNumber,cellSize *cellNumber+50)                      # Define the HUD area
    pygame.draw.rect(screen, (125,125,125), hud)                                                                # Draw the HUD background
    draw_text(mainGame.player.name + " are player " + str(mainGame.player.id + 1), mainGame.map.use_color[mainGame.player.id+1], 20, cellSize *cellNumber+12)# Show player information

    draw_text("(Press Arrow Keys or 'W','A','S','D' to move)", mainGame.map.use_color[mainGame.player.id+1], 250, cellSize *cellNumber+12)# Show movement instructions
    
    pygame.display.update()
    clock.tick(60)                                                                                              #60 frame/second add comments properly