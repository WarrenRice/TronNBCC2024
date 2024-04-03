import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1110
SCREEN_HEIGHT = 800

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("- Tron Multiplayer Lobby -")

# Font
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def draw_rounded_rect(surface, color, rect, radius=20):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_button(text, rect, color, text_color, radius=20):
    draw_rounded_rect(screen, color, rect, radius)
    draw_text(text, text_color, rect.x + 10, rect.y + 10)

def main():
    while True:
        screen.fill(BLACK)

        # Draw rounded corner buttons
        connect_button_rect = pygame.Rect(50, 450, 200, 50)
        draw_button("Connect", connect_button_rect, GREEN, WHITE)

        reset_button_rect = pygame.Rect(50, 700, 200, 50)
        draw_button("Reset", reset_button_rect, RED, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main()
