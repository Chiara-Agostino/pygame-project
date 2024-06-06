"""
Author: YOUR NAME
Date: YYYY-MM-DD
Description: Description of your program here.
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Window")

# Define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize more variables and states below
space_background = pygame.image.load("spacebackground.jpeg").convert()
space_background = pygame.transform.scale(space_background, (WIDTH, HEIGHT))

astronaut = pygame.image.load("sprite_1.png").convert_alpha()
astronaut_rect = astronaut.get_rect()  
astronaut_rect.midbottom = (WIDTH // 2, HEIGHT)

def moving():
    if keys[pygame.K_LEFT]:
        astronaut_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        astronaut_rect.x += 5

    if astronaut_rect.x < 0:
        astronaut_rect.x = 0
    if astronaut_rect.x > WIDTH - astronaut_rect.width:
        astronaut_rect.x = WIDTH - astronaut_rect.width


# Define main loop
running = True
clock = pygame.time.Clock()  # Initialize clock object to cap frame rate

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state
    screen.blit(space_background, (0, 0))
    screen.blit(astronaut, astronaut_rect)

    # Draw graphics and output
    keys = pygame.key.get_pressed()
    moving()



    # Update display
    pygame.display.flip()
    clock.tick(30)  # Limit frame rate to 30 fps

# Quit Pygame   
pygame.quit()
sys.exit()
