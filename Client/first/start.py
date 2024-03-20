import socket
import subprocess
import sys
import threading

import pygame


# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1110
SCREEN_HEIGHT = 800

PROPERTY_DELIMETER = "▐";

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("-Tron Multiplayer Lobby-")

# Load images
background_image = pygame.image.load("Tron2.jpg").convert()  # Replace "Tron2.jpg" with your actual image file path
green_tick_image = pygame.image.load("Green.png").convert_alpha()  # Replace "green_tick.png" with your green tick image file path
red_tick_image = pygame.image.load("Red.png").convert_alpha()  # Replace "red_tick.png" with your red tick image file path

# Font
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (75, 75, 255)
YELLOW = (255, 255, 0)

id = 0
posX = -1
posY = -1

def draw_text(ip_text, ip_color, x, y):
    ip_text_surface = font.render(ip_text, True, ip_color)
    screen.blit(ip_text_surface, (x, y))


def get_players_status(ip, port):
    global id;
    try:

        # Create a socket object
        '''
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        client_socket.connect((ip, port))
        
        print("Connected to the server and getting players")
        
        # Send player information to the server
        text = "GET_PLAYERS\n"
        client_socket.sendall(text.encode())
        
        data = client_socket.recv(1024)
        print(data.decode())
        
        string_data = data.decode()
        '''
        
        
        string_data = "N,0,0▐A,0,39▐B,39,0▐N,39,39▐"
        
        # Split the string using the separator '▐'
        split_data = string_data.split('▐')
        
        # Split each substring by ','
        split_data = [sub.split(',') for sub in split_data if sub]  # Exclude empty strings
        
        print(split_data)
            
        
        draw_text("LOBBY ", WHITE, 500, 340)
        draw_text("STATUS ", WHITE, 640, 340)
        
        
        draw_text("you" if id == 0 else "Player 1", RED, 500, 380)
        draw_text("you" if id == 1 else "Player 2", GREEN, 500, 420)
        draw_text("you" if id == 2 else "Player 3", BLUE, 500, 460)
        draw_text("you" if id == 3 else "Player 4", YELLOW, 500, 500)

        screen.blit(red_tick_image, (670, 380))  
        screen.blit(red_tick_image, (670, 420)) 
        screen.blit(red_tick_image, (670, 460))  
        screen.blit(red_tick_image, (670, 500)) 

        
        # Start a new thread to receive messages from the server
        #receive_thread = threading.Thread(target=receive_from_server, args=(client_socket,))
        #receive_thread.start()
        
        '''client_socket.close()'''
       
    except Exception as e:
        print("Connection error:", e)
    
def set_ready(ip, port):
    try:

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        client_socket.connect((ip, port))
        
        print("Connected to the server and setting players")
        
        # Send player information to the server
        text = "READY" + PROPERTY_DELIMETER + str(id) + "\n"
        client_socket.sendall(text.encode())
        
        data = client_socket.recv(1024)
        print(data.decode())
        
        # Start a new thread to receive messages from the server
        #receive_thread = threading.Thread(target=receive_from_server, args=(client_socket,))
        #receive_thread.start()
        
        client_socket.close()
        return True
        
    except Exception as e:
        print("Connection error:", e)
        return None

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
        #text = "RESET\n"
        client_socket.sendall(text.encode())
        
        
        
        data = client_socket.recv(1024)
        print(data.decode())
        
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
        
        print("id:", id)
        print("posX:", posX)
        print("posY:", posY)
                

        client_socket.close()
        return True
        
    except Exception as e:
        print("Connection error:", e)
        return None

def main():
    global id, posX, posY
    
    # Initialize variables
    state = "start"
    connect = False
    ready = False


    ip_input_box = pygame.Rect(250, 345, 140, 36)
    ip_color_inactive = pygame.Color('gray')
    ip_color_active = pygame.Color('yellow')
    ip_color = ip_color_inactive
    ip_active = False
    ip_text = '25.42.224.13'

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

        # Draw Connect Button5
        pygame.draw.rect(screen, connect_button_color, connect_button_rect)
        draw_text(connect_button_text, connect_button_text_color, 100, 460)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ip_input_box.collidepoint(event.pos):
                    ip_active = not ip_active
                    port_active = False
                elif port_input_box.collidepoint(event.pos):
                    port_active = not port_active
                    ip_active = False
                elif connect_button_rect.collidepoint(event.pos):
                    if ip_text and port_text and connect == False:
                        if connect_to_server(ip_text, int(port_text)):
                            state = "connected"
                            connect = True
                            connect_button_color = (0, 255, 0) if connect else (255, 0, 0)
                            connect_button_text = "Connected"
                            connect_button_text_color = BLACK

                        
                elif ready_button_rect.collidepoint(event.pos):
                        if state == "connected":
                            state = "ready"
                            
                            set_ready(ip_text, int(port_text))
                            
                            ready = True
                            ready_button_color = (0, 255, 0) if ready else (255, 0, 0)
                            ready_button_text = "Wait..."
                            ready_button_text_color = BLACK
                        
                else:
                    ip_active = False
                    port_active = False
                ip_color = ip_color_active if ip_active else ip_color_inactive
                port_color = port_color_active if port_active else port_color_inactive

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
        

        if state == "connected":
            # Draw Ready Button
            pygame.draw.rect(screen, ready_button_color, ready_button_rect)
            draw_text(ready_button_text, ready_button_text_color, 800, 710)
            
            get_players_status(ip_text, int(port_text))
            


            
        elif state == "ready":
            # Draw Ready Button
            pygame.draw.rect(screen, ready_button_color, ready_button_rect)
            draw_text(ready_button_text, ready_button_text_color, 800, 710)
            
            screen.blit(green_tick_image, (670, 380))  # Top-left
            screen.blit(red_tick_image, (670, 420))  # Top-right
            screen.blit(green_tick_image, (670, 460))  # Bottom-left
            screen.blit(red_tick_image, (670, 500))  # Bottom-right



        # Update the display
        pygame.display.flip()
        
if __name__ == "__main__":
    main()