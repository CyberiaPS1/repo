import pygame
import sys
import time

import config
import gameclient
import gameloop
from objects.entities import player

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Slimeboi")




# Initialize score
score = 0
font = pygame.font.Font(None, 36)


# Function to draw the score
def draw_score(screen, score):
    score_surface = font.render(f"Score: {score}", True, (255, 0, 0))
    screen.blit(score_surface, (10, 10))  # Position the score in the top-left corner




# Managing Game

client = None
loop_client = None

def new_game():
    global client, loop_client
    client = gameclient.GameClient()
    loop_client = gameloop.Gameloop(client, config.TICKRATE, time.time())




## Begin Debug FPS
accumulator = 0
time_prev = time.time()
fps_real = 0
fps_real_accumulator = 0
fps_tick = 0
fps_tick_accumulator = 0
## End   Debug FPS


# Create a Game
new_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_F2]:
        new_game()
    if keys[pygame.K_F3]:
        config.DEBUG = not config.DEBUG
    
    loop_count = loop_client.tick(time.time())
    client.draw(screen)
    
    # Draw the score
    draw_score(screen, score)

    # Draw the FPS
    if config.DEBUG:
        fps_real_accumulator += 1
        fps_tick_accumulator += loop_count

        time_current = time.time()
        frame_time = time_current - time_prev
        time_prev = time_current
        accumulator += frame_time
        if accumulator >= 1:
            accumulator = 0
            fps_real = fps_real_accumulator
            fps_real_accumulator = 0
            fps_tick = fps_tick_accumulator
            fps_tick_accumulator = 0

        fps_real_text = font.render("Real: "+str(fps_real), 1, pygame.Color(255, 0, 0))
        screen.blit(fps_real_text, (400,0))
        fps_tick_text = font.render("Tick: "+str(fps_tick), 1, pygame.Color(255, 0, 0))
        screen.blit(fps_tick_text, (600,0))

    # Update the display
    pygame.display.flip()


pygame.quit()
sys.exit()
