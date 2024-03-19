import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT_SIZE = 24
DROPDOWN_WIDTH = 200
DROPDOWN_HEIGHT = 40

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# Function to draw a dropdown box
def draw_dropdown(screen, font, options, x, y):
    # Draw dropdown box
    pygame.draw.rect(screen, WHITE, (x, y, DROPDOWN_WIDTH, DROPDOWN_HEIGHT), 2)
    draw_text("Select", font, BLACK, screen, x + 10, y + 10)

    # Draw options
    for i, option in enumerate(options):
        option_y = y + DROPDOWN_HEIGHT + i * DROPDOWN_HEIGHT
        pygame.draw.rect(screen, WHITE, (x, option_y, DROPDOWN_WIDTH, DROPDOWN_HEIGHT), 2)
        draw_text(option, font, BLACK, screen, x + 10, option_y + 10)

# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Dropdown Box")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, FONT_SIZE)
    options = ["Option 1", "Option 2", "Option 3"]
    dropdown_visible = False

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    dropdown_rect = pygame.Rect(10, 50, DROPDOWN_WIDTH, DROPDOWN_HEIGHT)
                    if dropdown_rect.collidepoint(mouse_pos):
                        dropdown_visible = not dropdown_visible

        # Draw dropdown box
        draw_dropdown(screen, font, options, 10, 50)

        # Draw dropdown options if visible
        if dropdown_visible:
            for i, option in enumerate(options):
                option_y = 90 + i * DROPDOWN_HEIGHT
                pygame.draw.rect(screen, WHITE, (10, option_y, DROPDOWN_WIDTH, DROPDOWN_HEIGHT), 2)
                draw_text(option, font, BLACK, screen, 20, option_y + 10)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
