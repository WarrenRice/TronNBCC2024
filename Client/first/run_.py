import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1110
SCREEN_HEIGHT = 500

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tron Multiplayer Lobby")

# Load background image
background_image = pygame.image.load("Tron2.jpg").convert()  # Replace "Tron2.jpg" with your actual image file path

# Load tick images
green_tick_image = pygame.image.load("Green.png").convert_alpha()  # Replace "green_tick.png" with your green tick image file path
red_tick_image = pygame.image.load("Red.png").convert_alpha()  # Replace "red_tick.png" with your red tick image file path

# Font
font = pygame.font.Font(None, 36)



def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def connect_to_server():
    pass


def main():
    # Initialize variables
    ready = False

    # Text input box for IP address
    ip_input_rect = pygame.Rect(50, 380, 200, 32)
    ip_input_active = False
    ip_input_text = ''
    ip_input_color_inactive = pygame.Color('lightskyblue3')
    ip_input_color_active = pygame.Color('dodgerblue2')
    ip_input_color = ip_input_color_inactive

    # Text input box for username
    username_input_rect = pygame.Rect(270, 380, 200, 32)
    username_input_active = False
    username_input_text = ''
    username_input_color_inactive = pygame.Color('lightskyblue3')
    username_input_color_active = pygame.Color('dodgerblue2')
    username_input_color = username_input_color_inactive

    # Ready button
    ready_button_rect = pygame.Rect(500, 370, 200, 50)
    ready_button_color = (0, 255, 0) if ready else (255, 0, 0)

    # Color options
    color_options = [pygame.Color('red'), pygame.Color('blue'), pygame.Color('yellow'), pygame.Color('green')]
    selected_color_index = 2

  

    # Main loop
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse is clicked within the input boxes
                if ip_input_rect.collidepoint(event.pos):
                    ip_input_active = not ip_input_active
                    username_input_active = False
                elif username_input_rect.collidepoint(event.pos):
                    username_input_active = not username_input_active
                    ip_input_active = False
                elif ready_button_rect.collidepoint(event.pos):
                    # Start the game when the "READY" button is clicked
                    if ip_input_text and username_input_text:  # Check if both IP and username are provided
                        # Launch game.py with IP address and username as arguments
                        subprocess.Popen(["python", "game.py", ip_input_text, username_input_text])
                        pygame.quit()
                        sys.exit()
                else:
                    ip_input_active = False
                    username_input_active = False
            elif event.type == pygame.KEYDOWN:
                # Handle key presses when text input boxes are active
                if ip_input_active:
                    if event.key == pygame.K_RETURN:
                        # Perform action when Enter is pressed in the IP address input box
                        pass  # Placeholder action
                    elif event.key == pygame.K_BACKSPACE:
                        ip_input_text = ip_input_text[:-1]
                    else:
                        ip_input_text += event.unicode
                elif username_input_active:
                    if event.key == pygame.K_RETURN:
                        # Perform action when Enter is pressed in the username input box
                        pass  # Placeholder action
                    elif event.key == pygame.K_BACKSPACE:
                        username_input_text = username_input_text[:-1]
                    else:
                        username_input_text += event.unicode

        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Draw UI elements
        draw_text("Enter IP Address:", WHITE, 50, 350)
        draw_text("Enter User ID:", WHITE, 270, 350)

        # Draw IP address input box
        ip_input_color = ip_input_color_active if ip_input_active else ip_input_color_inactive
        pygame.draw.rect(screen, ip_input_color, ip_input_rect, 2)
        draw_text(ip_input_text, WHITE, ip_input_rect.x + 5, ip_input_rect.y + 5)

        # Draw username input box
        username_input_color = username_input_color_active if username_input_active else username_input_color_inactive
        pygame.draw.rect(screen, username_input_color, username_input_rect, 2)
        draw_text(username_input_text, WHITE, username_input_rect.x + 5, username_input_rect.y + 5)

        # Draw ready button
        pygame.draw.rect(screen, ready_button_color, ready_button_rect)
        draw_text("READY", WHITE, 550, 380)

        # Draw color selection buttons horizontally
        color_button_size = 50
        color_button_spacing = 10
        color_button_x = 740
        color_button_y = 370
        for i, color in enumerate(color_options):
            rect = pygame.Rect(color_button_x + (color_button_size + color_button_spacing) * i, color_button_y, color_button_size, color_button_size)
            pygame.draw.rect(screen, color, rect)
            if i == selected_color_index:
                pygame.draw.rect(screen, BLACK, rect, 2)

        # Draw player numbers on the four sides of the screen
        draw_text("Player 1", WHITE, 10, 10)
        draw_text("Player 2", WHITE, SCREEN_WIDTH - 100, 10)
        draw_text("Player 3", WHITE, 10, SCREEN_HEIGHT - 40)
        draw_text("Player 4", WHITE, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40)

        # Draw tick and cross icons
        screen.blit(green_tick_image, (120, 10))  # Top-left
        screen.blit(red_tick_image, (SCREEN_WIDTH - 140, 10))  # Top-right
        screen.blit(green_tick_image, (120, SCREEN_HEIGHT - 40))  # Bottom-left
        screen.blit(red_tick_image, (SCREEN_WIDTH - 140, SCREEN_HEIGHT - 40))  # Bottom-right

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
