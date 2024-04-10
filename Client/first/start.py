import socket
import sys
import pygame
import subprocess
#from first.gameColor import COLORS
try: 
    from first.gameColor import COLORS
except Exception as e:
    pass
    
try: 
    from gameColor import COLORS
except Exception as e:
    pass

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1110
SCREEN_HEIGHT = 800


PROPERTY_DELIMETER = "▐";                                                                          # Define delimiter for network communication

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("-- Tron Multiplayer Lobby --")                                         # Set window caption

# Load images 
background_image = pygame.image.load("Tron2.jpg").convert()                                        # Load and convert background image
green_tick_image = pygame.image.load("Green.png").convert_alpha()                                  # Load and convert green tick image with alpha
red_tick_image = pygame.image.load("Red.png").convert_alpha()                                      # Load and convert red tick image with alpha

# Font
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
use_color = COLORS()

# Player and game state initialization

id = -1
posX = -1
posY = -1
name = ""
arguments = ["","","","","",""]                                                                     # Prepare arguments list for subprocess


def draw_text(ip_text, ip_color, x, y):                                                             # Function to draw text on the screen at specified coordinates

    ip_text_surface = font.render(ip_text, True, ip_color)                                          
    screen.blit(ip_text_surface, (x, y))                                                            


def get_players_status(ip, port):                                                                   # Function to get player status
    global id, start_game;
    try:

        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                            
        
        client_socket.connect((ip, port))                                                            
        
        
        text = "GET_PLAYERS\n"                                                                       # Command to get players' status
        client_socket.sendall(text.encode())                                                         # Send the command to the server
        
        data = client_socket.recv(1024)                                                              # Receive data from the server
        #print(data.decode())
        string_data = data.decode()                                                                  # Decode data to string

        split_data = string_data.split('▐')                                                          # Split received data at the delimiter
        
        split_data = [sub.split(',') for sub in split_data if sub]                                   # Further split each piece of data at commas
        
        split_data = split_data[:-1]                                                                 # Remove the last empty element from the list

        draw_text("LOBBY ", WHITE, 500, 340)                                                         # Draw 'LOBBY' text
        draw_text("STATUS ", WHITE, 640, 340)                                                        # Draw 'STATUS' text
        
        for _ in range(len(split_data)):
            if (split_data[_][0] == "IGNORE"):                                                        # ignore player spot not filled
                continue
            player_name = split_data[_][1]
            draw_text(str(player_name) + " (You)" if id == _ else (player_name), use_color[_+1], 500, 380+_*40)    # Display player name
            screen.blit(green_tick_image if split_data[_][0] == "R" else red_tick_image, (670, 380+_*40))          # Display status image
        

        player_statuses = filter(lambda status: status[0] != "IGNORE", split_data)                                 # Start game if all players are ready
        player_statuses_list = list(player_statuses)

            
        #if all(sublist[0] == "R" for sublist in player_statuses) and all(sublist[0] != "NR" for sublist in player_statuses): #set start_game flag
        if all(sublist[0] == "R" for sublist in player_statuses_list) and len(player_statuses_list) > 1:            # When all player are ready  limit 4 start game
            #print(len(player_statuses_list))
            start_game = True



        client_socket.close()
       
    except Exception as e:
        print("get_players_status error:", e)
    
def set_ready(ip, port):                                                                                     # Function to send Player are ready
    
    try:

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        
        client_socket.connect((ip, port))
        
        text = "READY" + PROPERTY_DELIMETER + str(id) + "\n"                                                  # Prepare ready command

        client_socket.sendall(text.encode())                                                                  # Send the command to the server
        
        data = client_socket.recv(1024)                                                                       # Receive acknowledgment from the server
        
        client_socket.close()

        return True
        
    except Exception as e:
        print("Connection error:", e)
        return None

def connect_to_server(ip, port, _name):                                                                         # Function to connect to server
    global id, posX, posY
    
    try:
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        client_socket.connect((ip, port))
        
        #print("Connected to the server successfully!")
        text = "CONNECTION" + PROPERTY_DELIMETER + _name +"\n"                                                 # Prepare connection command
        #text = "CONNECTION" + "\n"
        
        client_socket.sendall(text.encode())                                                                   # Send the command to the server
        data = client_socket.recv(1024)                                                                        # Receive player data from the server
        #print(data.decode())
        string_data = data.decode()                                                                            # Decode data to string

        separator_index = string_data.index('▐')                                                               # Find the separator in the string

        id = int(string_data[:separator_index])                                                                # Extract player ID from the data
        pos_text = string_data[separator_index + 1:]                                                           # Extract position text from the data
        
        comma_index = pos_text.index(',')                                                                      # Find the comma in the position text
        
        posX = int(pos_text[:comma_index])                                                                     # Extract X position
        posY = int(pos_text[comma_index + 1:])                                                                 # Extract Y position
        
        #print("id:", id)
        #print("posX:", posX)
        #print("posY:", posY)
                

        client_socket.close()
        return True
        
    except Exception as e:
        print("Lobby Full:", e)
        return None
    
# TO reset server  
''' 
def reset_server(ip, port):
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        client_socket.connect((ip, port))
        
        #print("Connected to the server successfully!")
        
        # Send player information to the server
        text = "RESET\n"
        #text = "RESET\n"
        client_socket.sendall(text.encode())

        data = client_socket.recv(1024)
        #print(data.decode())

        client_socket.close()
        
    except Exception as e:
        print("Connection error:", e)
'''
           
def disconnect_server(ip, port):                                                                          # Function To Disconnect server         

    try:

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        client_socket.connect((ip, port))
        
        #print("Connected to the server and setting players")
        
        text = "DISCONNECTED" + PROPERTY_DELIMETER + str(id) + "\n"                                     # Prepare disconnection command
        #print(text)
        client_socket.sendall(text.encode())
        
        data = client_socket.recv(1024)
        #print(data.decode())
        
        client_socket.close()
        
    except Exception as e:
        print("disconnect_server error:", e)

def draw_rounded_rect(surface, color, rect, radius=10):                                                  # Draw a rectangle with rounded corners
    pygame.draw.rect(surface, color, rect, border_radius=radius) 
    

def draw_button_with_rounded_corners(text, rect, color, text_color, offsetX, radius=10):                 # Function help to make rounded corner and txt color 
    draw_rounded_rect(screen, color, rect, radius)
    draw_text(text, text_color, rect.x + offsetX, rect.y + 12) 
    
def main():                                                                                              # Main function controlling the lobby interface and logic

    global id, posX, posY, start_game, name, arguments                                                   # Initialize the main variables for the lobby state

    
    state = "start"                                                                                      # Initial state of the lobby
    connect = False                                                                                      # Flag to indicate if the player is connected
    ready = False                                                                                        # Flag to indicate if the player is ready
    start_game = False                                                                                   # Flag to indicate if the game should start
    no_name = False                                                                                     # Flag to indicate if the player has not entered a name
    lobby_full = False                                                                                   # Flag to indicate if the lobby is full


    ip_input_box = pygame.Rect(250, 345, 140, 36)                                                        # Setup input boxes for IP
    ip_color_inactive = pygame.Color('gray')
    ip_color_active = pygame.Color('yellow')
    ip_color = ip_color_inactive
    ip_active = False
    #ip_text = '25.42.224.13'
    #ip_text = '25.41.59.168'
    ip_text = 'localhost'
    # ip_text = '25.34.232.141'
    
    port_input_box = pygame.Rect(250, 395, 140, 36)                                                     # Setup input boxes for  port
    port_color_inactive = pygame.Color('gray')
    port_color_active = pygame.Color('yellow')
    port_color = port_color_inactive
    port_active = False
    port_text = '6066'
    

    name_input_box = pygame.Rect(250, 445, 140, 36)                                                     # Setup input boxes for  player name
    name_color_inactive = pygame.Color('gray')
    name_color_active = pygame.Color('yellow')
    name_color = port_color_inactive
    name_active = False
    name_text = name
    
    connect_button_rect = pygame.Rect(50, 500, 200, 50)                                                 # Connect button
    connect_button_color = (0, 255, 0) if connect else (255, 0, 0)
    connect_button_text = "Connect"
    connect_button_text_color = WHITE
    connect_button_text_offsetX = 50
    
    ready_button_rect = pygame.Rect(750, 700, 200, 50)                                                 # Ready button
    ready_button_color = (0, 255, 0) if connect else (255, 0, 0)
    ready_button_text = "Ready"
    ready_button_text_color = WHITE
    
    
    # Reset button
    #reset_button_rect = pygame.Rect(50, 700, 200, 50)
    #reset_button_color = (0, 255, 0) if connect else (255, 0, 0)
    #reset_button_text = "Reset"
    #reset_button_text_color = WHITE
    
    while True:                                                                                        # Main loop for the lobby interface

        screen.fill(BLACK)                                                                             # Clear the screen with black color
        screen.blit(background_image, (0, 0))                                                          # Draw the background image

        # Handling input boxes and drawing them on the screen

        draw_text("Enter Server IP:", WHITE, 50, 350)
        txt_surface = font.render(ip_text, True, WHITE)
        width = max(200, txt_surface.get_width()+10)
        ip_input_box.w = width
        screen.blit(txt_surface, (ip_input_box.x+5, ip_input_box.y+5))
        pygame.draw.rect(screen, ip_color, ip_input_box, 2)
        # Handling input boxes and drawing them on the screen

        draw_text("Enter Port:", WHITE, 50, 400)
        txt_surface = font.render(port_text, True, WHITE)
        width = max(200, txt_surface.get_width()+10)
        port_input_box.w = width
        screen.blit(txt_surface, (port_input_box.x+5, port_input_box.y+5))
        pygame.draw.rect(screen, port_color, port_input_box, 2)
        
        draw_text("Enter Name:", WHITE, 50, 450)
        txt_surface = font.render(name_text, True, WHITE)
        width = max(200, txt_surface.get_width()+10)
        name_input_box.w = width
        screen.blit(txt_surface, (name_input_box.x+5, name_input_box.y+5))
        pygame.draw.rect(screen, name_color, name_input_box, 2)

        # Handling buttons and their interactions

        draw_button_with_rounded_corners(connect_button_text, connect_button_rect, connect_button_color, connect_button_text_color, connect_button_text_offsetX, radius=10)

        #draw_button_with_rounded_corners(reset_button_text, reset_button_rect, reset_button_color, reset_button_text_color, 65, radius=10)
        
        # Event handling for user inputs

        for event in pygame.event.get():                                                           # Event handling loop
            if event.type == pygame.QUIT:                                                          # Check for quit event
                if not id == -1 :
                    disconnect_server(ip_text, int(port_text))                                     # Disconnect from the server if connected
                pygame.quit()
                sys.exit()
                
                # Input box and button interaction logic
   
            elif event.type == pygame.MOUSEBUTTONDOWN:                                             # Check for mouse button press
                if state == "start":                                                               # Check if the click is within the input boxes or buttons
                    if ip_input_box.collidepoint(event.pos):                                       # Check for click in IP input box
                        ip_active = not ip_active                                                  # Toggle the active state
                        port_active = False
                        name_active = False
                        
                    elif port_input_box.collidepoint(event.pos):                                   # Check for click in port input box
                        port_active = not port_active                                              # Toggle the active state
                        ip_active = False
                        name_active = False
                    
                    elif name_input_box.collidepoint(event.pos):                                   # Check for click in name input box
                        name_active = not name_active                                              # Toggle the active state
                        ip_active = False
                        port_active = False
                        
                    #elif reset_button_rect.collidepoint(event.pos):
                    #    reset_server(ip_text, int(port_text))
                    
                    elif connect_button_rect.collidepoint(event.pos):                              # Check for click on connect button
                        if ip_text and port_text and connect == False:                             # Ensure IP and port are entered
                            if name_text:                                                          # Check if the name is entered
                                no_name = False
                                if connect_to_server(ip_text, int(port_text), name_text):          # Attempt to connect to the server
                                    state = "connected"                                            # Update state to connected
                                    connect = True                                                 # Set connect flag to True
                                    connect_button_color = (0, 255, 0) if connect else (255, 0, 0)
                                    connect_button_text = "Connected"
                                    connect_button_text_color = BLACK
                                    connect_button_text_offsetX = 40
                                    lobby_full = False
                                else:
                                    lobby_full = True
                            else:
                                no_name = True

                elif ready_button_rect.collidepoint(event.pos):                                     # Check for click on ready button
                        if state == "connected":
                            state = "ready"
                            
                            set_ready(ip_text, int(port_text))                                      # Set the player's status to ready
                            get_players_status(ip_text, int(port_text))                             # Get the players' status
                            
                            ready = True
                            ready_button_color = (0, 255, 0) if ready else (255, 0, 0)
                            ready_button_text = "Wait..."
                            ready_button_text_color = BLACK
                        
                else:
                    ip_active = False
                    port_active = False
                    name_active = False
                    
                ip_color = ip_color_active if ip_active else ip_color_inactive                      # Check for key press event
                port_color = port_color_active if port_active else port_color_inactive              # Check if IP input box is active
                name_color = name_color_active if name_active else name_color_inactive              # Remove the last character
                
            if event.type == pygame.KEYDOWN:                                                        # Add the pressed key to the IP text
                if ip_active:                                                                       # Check if Ip input box is active
                    if event.key == pygame.K_BACKSPACE:                                
                        ip_text = ip_text[:-1]                                                      # Remove the last character
                    else:                                   
                        ip_text += event.unicode                                                    # Add the pressed key to the IP text
                elif port_active:                                                                   # Check if port input box is active
                    if event.key == pygame.K_BACKSPACE:                                
                        port_text = port_text[:-1]                                                  # Remove the last character
                    elif event.unicode.isdigit():                                                   # Add the pressed key to the Port text                                 
                        port_text += event.unicode
                elif name_active:                                                                   # Check if name input box is active
                    if event.key == pygame.K_BACKSPACE:                                
                        name_text = name_text[:-1]                                                  # Remove the last character
                    else:                                   
                        name_text += event.unicode                                                  # Add the pressed key to the name text
                        

        if state == "connected":                                                                    # Check if the current state is connected

            draw_button_with_rounded_corners(ready_button_text, ready_button_rect, ready_button_color, ready_button_text_color, 60, radius=10)

            get_players_status(ip_text, int(port_text))                                             # Update players' status
 
        elif state == "ready":                                                                      # Check if the current state is ready

            draw_button_with_rounded_corners(ready_button_text, ready_button_rect, ready_button_color, ready_button_text_color, 60, radius=10)

            get_players_status(ip_text, int(port_text))                                             # Update players' status
            
            if (start_game == True):
                state = "start_game"                                                                # Check if the game should start
            
        elif state == "start_game":                                                                 # Check if the current state is to start the game
            arguments = [ str(id) , str(posX) , str(posY) , str(ip_text), str(port_text), str(name_text)]# Prepare arguments for the game
            
            #subprocess.run(["py", "game.py"] + arguments)
            subprocess.Popen(["py", "game.py"] + arguments)                                         # Start the game process

            pygame.quit()
            sys.exit()
            
        # Display warnings if the name is not filled or the lobby is full
         
        if no_name:
            draw_text("Name must be filled...", WHITE, 50, 570)
        elif lobby_full:
            draw_text("Lobby is full...", WHITE, 50, 570)

        # Update the display
        pygame.display.flip()
        
if __name__ == "__main__":
    main() 