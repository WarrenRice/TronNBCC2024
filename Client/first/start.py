import socket
import sys
import pygame
import subprocess
#from first.gameColor import COLORS
try: 
    from first.gameColor import COLORS
except Exception as e:
    from gameColor import COLORS


#ADD NAME
#AFTER CONNECTION BUG
#NOTICE WHEN EMPTY NAME
#NOTICE WHEN LOBBY FULL


#TODO
#Add Comments 
#Remove Reset
#Call RESET When game is over
#Don't Start When There is only one player


# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1110
SCREEN_HEIGHT = 800

PROPERTY_DELIMETER = "▐";

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("- Tron Multiplayer Lobby 6-")

# Load images
background_image = pygame.image.load("Tron2.jpg").convert()  
green_tick_image = pygame.image.load("Green.png").convert_alpha() 
red_tick_image = pygame.image.load("Red.png").convert_alpha()  

# Font
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
use_color = COLORS()

id = -1
posX = -1
posY = -1
name = ""
arguments = ["","","","","",""]

def draw_text(ip_text, ip_color, x, y):
    ip_text_surface = font.render(ip_text, True, ip_color)
    screen.blit(ip_text_surface, (x, y))


def get_players_status(ip, port):
    global id, start_game;
    try:

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        client_socket.connect((ip, port))
        
        #print("Connected to the server and getting players")
        
        # Send player information to the server
        text = "GET_PLAYERS\n"
        client_socket.sendall(text.encode())
        
        data = client_socket.recv(1024)
        #print(data.decode())
        
        string_data = data.decode()

        
        # Split the string using the separator '▐'
        split_data = string_data.split('▐')
        
        # Split each substring by ','
        split_data = [sub.split(',') for sub in split_data if sub]  # Exclude empty strings
        
        # Remove the last element from the list
        split_data = split_data[:-1]
        
        draw_text("LOBBY ", WHITE, 500, 340)
        draw_text("STATUS ", WHITE, 640, 340)
        
        for _ in range(len(split_data)):
            if (split_data[_][0] == "IGNORE"): # ignore player spot not filled
                continue
            player_name = split_data[_][1]
            draw_text("you" if id == _ else (player_name), use_color[_+1], 500, 380+_*40)
            screen.blit(green_tick_image if split_data[_][0] == "R" else red_tick_image, (670, 380+_*40))
        

        player_statuses = filter(lambda status: status[0] != "IGNORE", split_data)
        if all(sublist[0] == "R" for sublist in player_statuses) and all(sublist[0] != "NR" for sublist in player_statuses): #set start_game flag
            start_game = True

        client_socket.close()
       
    except Exception as e:
        print("get_players_status error:", e)
    
def set_ready(ip, port):
    try:

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        client_socket.connect((ip, port))
        
        #print("Connected to the server and setting players")
        
        # Send player information to the server
        text = "READY" + PROPERTY_DELIMETER + str(id) + "\n"
        #print(text)
        client_socket.sendall(text.encode())
        
        data = client_socket.recv(1024)
        #print(data.decode())
        
        client_socket.close()
        return True
        
    except Exception as e:
        print("Connection error:", e)
        return None

def connect_to_server(ip, port, _name):
    global id, posX, posY
    
    try:
        
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        client_socket.connect((ip, port))
        
        #print("Connected to the server successfully!")
        
        # Send player information to the server
        text = "CONNECTION" + PROPERTY_DELIMETER + _name +"\n"
        #text = "CONNECTION" + "\n"
        
        client_socket.sendall(text.encode())
        data = client_socket.recv(1024)
        
        #print(data.decode())
        
        string_data = data.decode()

        # Find the index of the separator character '▐'
        separator_index = string_data.index('▐')

        # Extract id, posX, and posY using string slicing
        id = int(string_data[:separator_index])
        pos_text = string_data[separator_index + 1:]
        
        # Find the index of the comma separator ','
        comma_index = pos_text.index(',')
        
        # Extract posX and posY
        posX = int(pos_text[:comma_index])
        posY = int(pos_text[comma_index + 1:])
        
        #print("id:", id)
        #print("posX:", posX)
        #print("posY:", posY)
                

        client_socket.close()
        return True
        
    except Exception as e:
        print("Lobby Full:", e)
        return None
    
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
        
def disconnect_server(ip, port):
    try:

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        client_socket.connect((ip, port))
        
        #print("Connected to the server and setting players")
        
        # Send player information to the server
        text = "DISCONNECTED" + PROPERTY_DELIMETER + str(id) + "\n"
        #print(text)
        client_socket.sendall(text.encode())
        
        data = client_socket.recv(1024)
        #print(data.decode())
        
        client_socket.close()
        
    except Exception as e:
        print("disconnect_server error:", e)

def draw_rounded_rect(surface, color, rect, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_button_with_rounded_corners(text, rect, color, text_color, offsetX, radius=10):
    draw_rounded_rect(screen, color, rect, radius)
    draw_text(text, text_color, rect.x + offsetX, rect.y + 12)

def main():
    global id, posX, posY, start_game, name, arguments
    
    # Initialize variables
    state = "start"
    connect = False
    ready = False
    start_game = False
    no_name = False
    lobby_full = False


    ip_input_box = pygame.Rect(250, 345, 140, 36)
    ip_color_inactive = pygame.Color('gray')
    ip_color_active = pygame.Color('yellow')
    ip_color = ip_color_inactive
    ip_active = False
    #ip_text = '25.42.224.13'
    #ip_text = '25.41.59.168'
    ip_text = 'localhost'
    # ip_text = '25.34.232.141'

    port_input_box = pygame.Rect(250, 395, 140, 36)
    port_color_inactive = pygame.Color('gray')
    port_color_active = pygame.Color('yellow')
    port_color = port_color_inactive
    port_active = False
    port_text = '6066'
    
    name_input_box = pygame.Rect(250, 445, 140, 36)
    name_color_inactive = pygame.Color('gray')
    name_color_active = pygame.Color('yellow')
    name_color = port_color_inactive
    name_active = False
    name_text = name
    
    # Connect button
    connect_button_rect = pygame.Rect(50, 500, 200, 50)
    connect_button_color = (0, 255, 0) if connect else (255, 0, 0)
    connect_button_text = "Connect"
    connect_button_text_color = WHITE
    connect_button_text_offsetX = 50
    
    # Ready button
    ready_button_rect = pygame.Rect(750, 700, 200, 50)
    ready_button_color = (0, 255, 0) if connect else (255, 0, 0)
    ready_button_text = "Ready"
    ready_button_text_color = WHITE
    
    
    # Reset button
    reset_button_rect = pygame.Rect(50, 700, 200, 50)
    reset_button_color = (0, 255, 0) if connect else (255, 0, 0)
    reset_button_text = "Reset"
    reset_button_text_color = WHITE
    
    while True:
        # Draw the background image
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        
        # Draw UI elements
        #Player Input Box
        draw_text("Enter Server IP:", WHITE, 50, 350)
        txt_surface = font.render(ip_text, True, WHITE)
        width = max(200, txt_surface.get_width()+10)
        ip_input_box.w = width
        screen.blit(txt_surface, (ip_input_box.x+5, ip_input_box.y+5))
        pygame.draw.rect(screen, ip_color, ip_input_box, 2)
        
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

        # Draw Buttons
        draw_button_with_rounded_corners(connect_button_text, connect_button_rect, connect_button_color, connect_button_text_color, connect_button_text_offsetX, radius=10)

        draw_button_with_rounded_corners(reset_button_text, reset_button_rect, reset_button_color, reset_button_text_color, 65, radius=10)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not id == -1 :
                    disconnect_server(ip_text, int(port_text))
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "start":
                    if ip_input_box.collidepoint(event.pos):
                        ip_active = not ip_active
                        port_active = False
                        name_active = False
                        
                    elif port_input_box.collidepoint(event.pos):
                        port_active = not port_active
                        ip_active = False
                        name_active = False
                    
                    elif name_input_box.collidepoint(event.pos):
                        name_active = not name_active
                        ip_active = False
                        port_active = False
                        
                    elif reset_button_rect.collidepoint(event.pos):
                        reset_server(ip_text, int(port_text))
                    
                    elif connect_button_rect.collidepoint(event.pos):
                        if ip_text and port_text and connect == False:
                            if name_text:
                                no_name = False
                                if connect_to_server(ip_text, int(port_text), name_text):
                                    state = "connected"
                                    connect = True
                                    connect_button_color = (0, 255, 0) if connect else (255, 0, 0)
                                    connect_button_text = "Connected"
                                    connect_button_text_color = BLACK
                                    connect_button_text_offsetX = 40
                                    lobby_full = False
                                else:
                                    lobby_full = True
                            else:
                                no_name = True

                elif ready_button_rect.collidepoint(event.pos):
                        if state == "connected":
                            state = "ready"
                            
                            set_ready(ip_text, int(port_text))
                            get_players_status(ip_text, int(port_text))
                            
                            ready = True
                            ready_button_color = (0, 255, 0) if ready else (255, 0, 0)
                            ready_button_text = "Wait..."
                            ready_button_text_color = BLACK
                        
                else:
                    ip_active = False
                    port_active = False
                    name_active = False
                ip_color = ip_color_active if ip_active else ip_color_inactive
                port_color = port_color_active if port_active else port_color_inactive
                name_color = name_color_active if name_active else name_color_inactive

            if event.type == pygame.KEYDOWN:
                if ip_active:
                    if event.key == pygame.K_BACKSPACE:                                
                        ip_text = ip_text[:-1]
                    else:                                   
                        ip_text += event.unicode
                elif port_active:
                    if event.key == pygame.K_BACKSPACE:                                
                        port_text = port_text[:-1]
                    elif event.unicode.isdigit():                                   
                        port_text += event.unicode
                elif name_active:
                    if event.key == pygame.K_BACKSPACE:                                
                        name_text = name_text[:-1]
                    else:                                   
                        name_text += event.unicode

        if state == "connected":
            # Draw Ready Button
            draw_button_with_rounded_corners(ready_button_text, ready_button_rect, ready_button_color, ready_button_text_color, 60, radius=10)

            get_players_status(ip_text, int(port_text))
 
        elif state == "ready":
            # Draw Ready Button
            draw_button_with_rounded_corners(ready_button_text, ready_button_rect, ready_button_color, ready_button_text_color, 60, radius=10)

            get_players_status(ip_text, int(port_text))
            
            if (start_game == True):
                state = "start_game"
            
        elif state == "start_game":
            arguments = [ str(id) , str(posX) , str(posY) , str(ip_text), str(port_text), str(name_text)]
            
            #subprocess.run(["py", "game.py"] + arguments)
            subprocess.Popen(["py", "game.py"] + arguments)
            pygame.quit()
            sys.exit()
               
        if no_name:
            draw_text("Name must be filled...", WHITE, 50, 570)
        elif lobby_full:
            draw_text("Lobby is full...", WHITE, 50, 570)

        # Update the display
        pygame.display.flip()
        
if __name__ == "__main__":
    main() 