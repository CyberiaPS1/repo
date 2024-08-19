import pygame
import config
import objects.entities.player

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Color for obstacles
LAYER2_COLOR = (0, 0, 0)  # Character color in layer 2
BACKGROUND_LAYER_COLOR = (50, 50, 50)  # Background color for layer 1
FOREGROUND_LAYER_COLOR = (100, 100, 100)  # Color for layer 2

class GameClient:
    def __init__(self):
        self.player = objects.entities.player.Player()
        self.obstacles = [
            pygame.Rect(200, 500, 125, 20),  # Example obstacle 1
            pygame.Rect(400, 450, 125, 20),  # Example obstacle 2
            pygame.Rect(600, 400, 125, 20),  # Example obstacle 3
            pygame.Rect(400, 75, 10, 100),
            pygame.Rect(0, 590, config.SCREEN_WIDTH, 10), # Floor
            pygame.Rect(0, 0, 10, config.SCREEN_HEIGHT),  # Left wall
            pygame.Rect(790, 0, 10, config.SCREEN_HEIGHT) # Right wall
        ]
    
    def draw(self, surface):
        # Draw Background
        surface.fill(BACKGROUND_LAYER_COLOR)
        layer2y = config.SCREEN_HEIGHT // 2
        pygame.draw.rect(surface, FOREGROUND_LAYER_COLOR, (0, layer2y, config.SCREEN_WIDTH, config.SCREEN_HEIGHT - layer2y))  # Layer 2 (foreground)

        # Draw Objects
        for obs in self.obstacles:
            pygame.draw.rect(surface, GREEN, obs)

        # Draw Entities
        self.player.draw(surface)
    
    def tick(self):

        # Inputs
        keys = pygame.key.get_pressed()

        # Player
        self.player.read_inputs(keys)
        self.player.process()
        self.player.move_and_collide(self.obstacles)