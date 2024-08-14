import pygame
import sys
import time
from objects.entities import player

# Initialize Pygame
pygame.init()

TARGET_FPS = 1 / 120

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Slimeboi")

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Color for obstacles
BACKGROUND_LAYER_COLOR = (50, 50, 50)  # Background color for layer 1
FOREGROUND_LAYER_COLOR = (100, 100, 100)  # Color for layer 2

# Define character properties
char_width, char_height = 50, 50
char_x, char_y = (screen_width - char_width) // 2, (screen_height - char_height) // 2
char_speed = 5
char_rect = pygame.Rect(char_x, char_y, char_width, char_height)
char_color = RED

# Initialize the Player object
oplayer = player.Player()

# Define obstacles
obstacles = [
    pygame.Rect(200, screen_height - 100, 150, 20),  # Example obstacle 1
    pygame.Rect(400, screen_height - 150, 150, 20),  # Example obstacle 2
    pygame.Rect(600, screen_height - 200, 150, 20),  # Example obstacle 3
    pygame.Rect(400, 75, 10, 100),
    pygame.Rect(0, 590, screen_width, 10), # Floor
    pygame.Rect(0, 0, 10, screen_height),  # Left wall
    pygame.Rect(790, 0, 10, screen_height) # Right wall
]

# Define layer boundaries
layer1_y = screen_height // 2  # Top half of the screen
layer2_y = screen_height // 2  # Bottom half of the screen

# Initialize score and in_layer2
score = 0
in_layer2 = False
font = pygame.font.Font(None, 36)

# Function to check if the character is in layer 2
def is_in_layer2(char_rect):
    return char_rect.bottom > layer2_y

# Function to check for collision
def check_collision(rect, obstacles):
    for obs in obstacles:
        if rect.colliderect(obs):
            return obs
    return None

# Function to draw the score
def draw_score(screen, score):
    score_surface = font.render(f"Score: {score}", True, RED)
    screen.blit(score_surface, (10, 10))  # Position the score in the top-left corner

# Main game loop
def gameloop():
    global in_layer2, score
    keys = pygame.key.get_pressed()

    oplayer.read_inputs(keys)
    oplayer.process()
    oplayer.move_and_collide(obstacles)

    # Get the time delta between frames
    delta_time = time.time() - time_prev

    # Update player animation
    oplayer.update_animation(delta_time)

    # Check if the character is in layer 2 and update score
    currently_in_layer2 = is_in_layer2(oplayer.rect)
    if currently_in_layer2 and not in_layer2:
        in_layer2 = True
    elif not currently_in_layer2 and in_layer2:
        in_layer2 = False

    if in_layer2:
        score += 1

    # Fill the screen with background color
    screen.fill(BACKGROUND_LAYER_COLOR)

    # Draw background layers
    pygame.draw.rect(screen, FOREGROUND_LAYER_COLOR, (0, layer2_y, screen_width, screen_height - layer2_y))  # Layer 2 (foreground)

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, GREEN, obs)

    # Draw the player sprite
    oplayer.draw(screen)

    # Draw the score
    draw_score(screen, score)

    # Update display
    pygame.display.flip()

# Set up a clock object to control the frame rate
clock = pygame.time.Clock()
time_prev = time.time()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Run the game loop
    gameloop()

    # Cap the frame rate
    clock.tick(120)
