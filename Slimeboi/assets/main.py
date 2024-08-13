import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Slimeboi")

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Color for obstacles
LAYER2_COLOR = (0, 0, 0)  # Character color in layer 2
BACKGROUND_LAYER_COLOR = (50, 50, 50)  # Background color for layer 1
FOREGROUND_LAYER_COLOR = (100, 100, 100)  # Color for layer 2

# Define character properties
char_width, char_height = 50, 50
char_x, char_y = (screen_width - char_width) // 2, (screen_height - char_height) // 2
char_speed = 0.1
char_velocity_y = 0  # Initialize vertical velocity for jumping
gravity = 0.0005  # Gravity strength (reduced to make the player fall more slowly)
jump_strength = -0.4  # Jumping strength
on_ground = False  # To check if the player is on the ground

# Define obstacles
obstacles = [
    pygame.Rect(200, screen_height - 100, 150, 20),  # Example obstacle 1
    pygame.Rect(400, screen_height - 150, 150, 20),  # Example obstacle 2
    pygame.Rect(600, screen_height - 200, 150, 20)   # Example obstacle 3
]

# Define layer boundaries
layer1_y = screen_height // 2  # Top half of the screen
layer2_y = screen_height // 2  # Bottom half of the screen

# Initialize score
score = 0
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
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Move character based on key presses
    if keys[pygame.K_LEFT]:
        char_x -= char_speed
    if keys[pygame.K_RIGHT]:
        char_x += char_speed
    if keys[pygame.K_UP]:
        char_y -= char_speed
    if keys[pygame.K_DOWN]:
        char_y += char_speed

    # Check for jumping with "O" button
    if keys[pygame.K_o] and on_ground:
        char_velocity_y = jump_strength

    # Apply gravity
    char_velocity_y += gravity
    char_y += char_velocity_y

    # Create a rectangle for the character
    char_rect = pygame.Rect(char_x, char_y, char_width, char_height)

    # Check for collision with obstacles
    collision = check_collision(char_rect, obstacles)
    if collision:
        # Simple collision response: stop movement when hitting an obstacle
        if keys[pygame.K_LEFT]:
            char_x += char_speed
        if keys[pygame.K_RIGHT]:
            char_x -= char_speed
        if keys[pygame.K_UP]:
            char_y += char_speed
        if keys[pygame.K_DOWN]:
            char_y -= char_speed

    # Constrain character within the screen boundaries
    if char_x < 0:
        char_x = 0
    elif char_x > screen_width - char_width:
        char_x = screen_width - char_width

    if char_y < 0:
        char_y = 0
    elif char_y > screen_height - char_height:
        char_y = screen_height - char_height

    # Check if the player is on the ground
    if char_y + char_height >= screen_height:
        char_y = screen_height - char_height
        char_velocity_y = 0
        on_ground = True
    else:
        on_ground = False

    # Fill the screen with background color
    screen.fill(BACKGROUND_LAYER_COLOR)

    # Draw background layers
    pygame.draw.rect(screen, FOREGROUND_LAYER_COLOR, (0, layer2_y, screen_width, screen_height - layer2_y))  # Layer 2 (foreground)

    # Determine character color based on layer position
    if is_in_layer2(char_rect):
        char_color = LAYER2_COLOR
    else:
        char_color = RED

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, GREEN, obs)

    # Draw the character with the appropriate color
    pygame.draw.rect(screen, char_color, char_rect)

    # Draw the score
    draw_score(screen, score)

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
