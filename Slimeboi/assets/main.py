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
LAYER2_COLOR = (0, 0, 0)  # Character color in layer 2
BACKGROUND_LAYER_COLOR = (50, 50, 50)  # Background color for layer 1
FOREGROUND_LAYER_COLOR = (100, 100, 100)  # Color for layer 2

# Define character properties
char_width, char_height = 50, 50
char_x, char_y = (screen_width - char_width) // 2, (screen_height - char_height) // 2
char_speed = 5
char_rect = pygame.Rect(char_x, char_y, char_width, char_height)
char_color = RED

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

# Initialize score
score = 0
font = pygame.font.Font(None, 36)

# Initialize layer state
in_layer2 = False

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
    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Character processing
    oplayer.read_inputs(keys)
    oplayer.process()
    oplayer.move_and_collide(obstacles)

    global char_rect, char_x, char_y, char_speed, in_layer2, score

    # Move character based on key presses
    if keys[pygame.K_LEFT]:
        char_x -= char_speed
    if keys[pygame.K_RIGHT]:
        char_x += char_speed
    if keys[pygame.K_UP]:
        char_y -= char_speed
    if keys[pygame.K_DOWN]:
        char_y += char_speed

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

    # Check if the character is in layer 2 and update score
    currently_in_layer2 = is_in_layer2(char_rect)
    if currently_in_layer2 and not in_layer2:
        # Entering layer 2
        in_layer2 = True
    elif not currently_in_layer2 and in_layer2:
        # Exiting layer 2
        in_layer2 = False

    if in_layer2:
        score += 1

    # Fill the screen with background color
    screen.fill(BACKGROUND_LAYER_COLOR)

    # Draw background layers
    pygame.draw.rect(screen, FOREGROUND_LAYER_COLOR, (0, layer2_y, screen_width, screen_height - layer2_y))  # Layer 2 (foreground)

    # Determine character color based on layer position
    if is_in_layer2(char_rect):
        char_color = LAYER2_COLOR
    else:
        char_color = RED

    


# Fixed Timestep
time_prev = time.time()
frame_time = 0
accumulator = 0
loops = 0
count = 0
second_accumulator = 0
fpsreal_accumulator = 0
fpstick_accumulator = 0
fps_real = 0
fps_tick = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    time_current = time.time()
    frame_time = time_current - time_prev
    accumulator += frame_time
    second_accumulator += frame_time
    fpsreal_accumulator += 1
    time_prev = time_current

    loops = accumulator // TARGET_FPS
    accumulator -= loops * TARGET_FPS
    while loops > 0:
        gameloop()
        loops -= 1
        fpstick_accumulator += 1
    
    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, GREEN, obs)

    # Draw the character with the appropriate color
    pygame.draw.rect(screen, char_color, char_rect)
    oplayer.draw(screen)

    # Draw the score
    draw_score(screen, score)

    # Draw the FPS
    if frame_time > 0:
        if second_accumulator >= 1:
            second_accumulator -= 1
            fps_real = fpsreal_accumulator
            fpsreal_accumulator = 0
            fps_tick = fpstick_accumulator
            fpstick_accumulator = 0

        fps_t = round(60.0 / (frame_time * 1000))
        fps_real_text = font.render(str(fps_real), 1, pygame.Color(255, 0, 0))
        screen.blit(fps_real_text, (200,0))
        fps_tick_text = font.render(str(fps_tick), 1, pygame.Color(255, 0, 0))
        screen.blit(fps_tick_text, (300,0))

    # Update the display
    pygame.display.flip()


pygame.quit()
sys.exit()
