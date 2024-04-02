import socket
import sys
import pygame
import subprocess
from first.gameColor import COLOR

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1110
SCREEN_HEIGHT = 800

# # Delimiter used for parsing data sent over the network
PROPERTY_DELIMETER = "▐";

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("- Tron Multiplayer Lobby -")

# Load images
background_image = pygame.image.load("Tron2.jpg").convert()  # Replace "Tron2.jpg" with your actual image file path
green_tick_image = pygame.image.load("Green.png").convert_alpha()  # Replace "green_tick.png" with your green tick image file path
red_tick_image = pygame.image.load("Red.png").convert_alpha()  # Replace "red_tick.png" with your red tick image file path

# Font
font = pygame.font.Font(None, 36)
border_radius = 15
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
use_color = COLOR()

# player id position x and y
id = -1
posX = -1
posY = -1

# Function to draw text on the screen
def draw_text(ip_text, ip_color, x, y):
    ip_text_surface = font.render(ip_text, True, ip_color)
    screen.blit(ip_text_surface, (x, y))


# Networking functions to interact with the server
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
            draw_text("you" if id == _ else ("Player" + str(_+1)), use_color[_+1], 500, 380+_*40)
            screen.blit(green_tick_image if split_data[_][0] == "R" else red_tick_image, (670, 380+_*40))
        
        #draw_text("you" if id == 0 else "Player 1", use_color[0], 500, 380)
        #draw_text("you" if id == 1 else "Player 2", use_color[1] if len(split_data) > 1 else BLACK, 500, 420)
        #draw_text("you" if id == 2 else "Player 3", use_color[2] if len(split_data) > 2 else BLACK, 500, 460)
        #draw_text("you" if id == 3 else "Player 4", use_color[3] if len(split_data) > 3 else BLACK, 500, 500)

        #screen.blit(green_tick_image if split_data[0][0] == "R" else red_tick_image, (670, 380))  
        #screen.blit(green_tick_image if split_data[1][0] == "R" else red_tick_image, (670, 420)) 
        #screen.blit(green_tick_image if split_data[2][0] == "R" else red_tick_image, (670, 460))  
        #screen.blit(green_tick_image if split_data[3][0] == "R" else red_tick_image, (670, 500))
        
        #if all(sublist[0] == "R" for sublist in split_data) and len(split_data):
        if all(sublist[0] == "R" for sublist in split_data): #set start_game flag
            start_game = True
        
        #print(start_game)
        
        #print(all(sublist[0] == "R" for sublist in split_data))
        

        client_socket.close()
       
    except Exception as e:
        print("get_players_status error:", e)
        
# Sends a signal to the server indicating that this player is ready.    
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
 # Establishes a connection to the game server and retrieves player ID and position.
def connect_to_server(ip, port):
    global id, posX, posY
    try:

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        client_socket.connect((ip, port))
        
        print("Connected to the server successfully!")
        
        # Send player information to the server
        text = "CONNECTION\n"
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
        print("Connection error:", e)
        return None
    
# Sends a command to the server to reset its state.    
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

def draw_rounded_button(rect, color, text, text_color, border_rad):
        # Draw the button with rounded corners
        pygame.draw.rect(screen, color, rect, border_radius=border_rad)
     
        # Draw the text on the button
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
       
# Main function of the script
def main():
    # VInitialize variables using enum states (id,position x and y and start game)
    global id, posX, posY, start_game
    
    # Initialize variables
    state = "start"
    connect = False
    ready = False
    start_game = False

    #Input box for ip 
    ip_input_box = pygame.Rect(250, 345, 140, 36)
    ip_color_inactive = pygame.Color('gray')
    ip_color_active = pygame.Color('yellow')
    ip_color = ip_color_inactive
    ip_active = False
    #ip_text = '25.42.224.13'
    # ip_text = '25.42.224.13'
    ip_text = 'localhost'
    
    
    #Input box for port
    port_input_box = pygame.Rect(250, 395, 140, 36)
    port_color_inactive = pygame.Color('gray')
    port_color_active = pygame.Color('yellow')
    port_color = port_color_inactive
    port_active = False
    port_text = '6066'
    
    
    # Connect button
    connect_button_rect = pygame.Rect(50, 450, 200, 50)
    connect_button_color = (0, 255, 0) if connect else (255, 0, 0)
    connect_button_text = "Connect"
    connect_button_text_color = WHITE
    
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
    # In your main loop or drawing function, replace the button drawing code with:
    draw_rounded_button(connect_button_rect, connect_button_color, connect_button_text, connect_button_text_color, border_radius)
    draw_rounded_button(ready_button_rect, ready_button_color, ready_button_text, ready_button_text_color, border_radius)
    draw_rounded_button(reset_button_rect, reset_button_color, reset_button_text, reset_button_text_color, border_radius)
    
       
    while True:
        # Draw the background image
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        
        # Draw UI elements for server IP input
        draw_text("Enter Server IP:", WHITE, 50, 350)  # Draw text for IP input
        txt_surface = font.render(ip_text, True, WHITE)  # Render the IP text input by the user
        width = max(200, txt_surface.get_width()+10)  # Calculate the width of the input box
        ip_input_box.w = width  # Update the width of the IP input box
        screen.blit(txt_surface, (ip_input_box.x+5, ip_input_box.y+5))  # Draw the text inside the IP input box
        pygame.draw.rect(screen, ip_color, ip_input_box, 2)  # Draw the IP input box

        draw_text("Enter Port:", WHITE, 50, 400)  # Draw text for Port input
        txt_surface = font.render(port_text, True, WHITE)  # Render the Port text input by the user
        width = max(200, txt_surface.get_width()+10)  # Calculate the width of the input box
        port_input_box.w = width  # Update the width of the Port input box
        screen.blit(txt_surface, (port_input_box.x+5, port_input_box.y+5))  # Draw the text inside the Port input box
        pygame.draw.rect(screen, port_color, port_input_box, 2)  # Draw the Port input box

        # Draw Connect and Reset buttons
        pygame.draw.rect(screen, connect_button_color, connect_button_rect)  # Draw Connect button
        draw_text(connect_button_text, connect_button_text_color, 100, 460)  # Draw text on Connect button
        pygame.draw.rect(screen, reset_button_color, reset_button_rect)  # Draw Reset button
        draw_text(reset_button_text, reset_button_text_color, 100, 710)  # Draw text on Reset button

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit the program
                sys.exit()  # Exit the system
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ip_input_box.collidepoint(event.pos):
                    ip_active = not ip_active  # Toggle active status of IP input
                    port_active = False  # Deactivate Port input
                elif port_input_box.collidepoint(event.pos):
                    port_active = not port_active  # Toggle active status of Port input
                    ip_active = False  # Deactivate IP input
                    
                elif reset_button_rect.collidepoint(event.pos):
                    reset_server(ip_text, int(port_text))# Reset the server with given IP and port
                
                elif connect_button_rect.collidepoint(event.pos):
                    if ip_text and port_text and connect == False:
                        if connect_to_server(ip_text, int(port_text)):
                            state = "connected"  # Change state to connected
                            connect = True  # Set connect flag to True
                            connect_button_color = (0, 255, 0) if connect else (255, 0, 0)  # Change Connect button color
                            connect_button_text = "Connected"  # Update Connect button text
                            connect_button_text_color = BLACK  # Set Connect button text color

                        
                elif ready_button_rect.collidepoint(event.pos):
                        if state == "connected":  # Ensure the current state is connected
                            state = "ready"  # Change state to ready
                            set_ready(ip_text, int(port_text))  # Mark as ready in the server
                            get_players_status(ip_text, int(port_text))  # Get the status of players from the server
                            ready = True  # Set ready flag to True
                            ready_button_color = (0, 255, 0) if ready else (255, 0, 0)  # Change Ready button color
                            ready_button_text = "Wait..."  # Update Ready button text
                            ready_button_text_color = BLACK  # Set Ready button text color
                else:#If clicked outside of interactive elements
                    ip_active = False  # Deactivate IP input
                    port_active = False # Deactivate Port input
                ip_color = ip_color_active if ip_active else ip_color_inactive # Update IP input box color
                port_color = port_color_active if port_active else port_color_inactive# Update Port input box color

            if event.type == pygame.KEYDOWN:  # Check for keyboard input
                if ip_active:  # If IP input is active
                    if event.key == pygame.K_BACKSPACE:  # Check if backspace is pressed
                        ip_text = ip_text[:-1]  # Remove the last character from IP text
                    else:  # If other keys are pressed
                        ip_text += event.unicode  # Add the typed character to IP text
                elif port_active:  # If Port input is active
                    if event.key == pygame.K_BACKSPACE:  # Check if backspace is pressed
                        port_text = port_text[:-1]  # Remove the last character from Port text
                    elif event.unicode.isdigit():  # Check if the typed character is a digit
                        port_text += event.unicode  # Add the typed digit to Port text

        if state == "connected":
            # Draw Ready Button
            pygame.draw.rect(screen, ready_button_color, ready_button_rect)
            draw_text(ready_button_text, ready_button_text_color, 800, 710)
            
            get_players_status(ip_text, int(port_text))
            


            
        elif state == "ready":
            # Draw Ready Button
            pygame.draw.rect(screen, ready_button_color, ready_button_rect)
            draw_text(ready_button_text, ready_button_text_color, 800, 710)

            get_players_status(ip_text, int(port_text))
            
            if (start_game == True):
                state = "start_game"# Change state to start_game
            
        elif state == "start_game":
            arguments = [ str(id) , str(posX) , str(posY) , str(ip_text), str(port_text)] # Prepare arguments for the game
            
            subprocess.Popen(["python", "game.py"] + arguments)# Start the game process
            pygame.quit()  # Quit the pygame
            sys.exit()# Exit the system

        # Update the display
        

if __name__ == "__main__":
    main()