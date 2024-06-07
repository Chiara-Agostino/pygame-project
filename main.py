"""
Author: YOUR NAME
Date: YYYY-MM-DD
Description: Description of your program here.
"""

import pygame
import sys
import random

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

spaceship_img = pygame.image.load("spaceship-3.png").convert_alpha()

def create_spaceship():
    x = random.randint(0, WIDTH - spaceship_img.get_width())
    y = -spaceship_img.get_height()
    rect = pygame.Rect(x, y, spaceship_img.get_width(), spaceship_img.get_height())
    return rect, spaceship_img

def move_spaceships(spaceships):
    for spaceship in spaceships:
        spaceship[0].y += 8
        if spaceship[0].top > HEIGHT:
            spaceship[0].x = random.randint(0, WIDTH - spaceship_img.get_width())
            spaceship[0].y = -spaceship_img.get_height()

def draw_spaceships(spaceships):
    for spaceship in spaceships:
        screen.blit(spaceship[1], spaceship[0])

def moving():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        astronaut_rect.x -= 7
    if keys[pygame.K_RIGHT]:
        astronaut_rect.x += 7

    if astronaut_rect.x < 0:
        astronaut_rect.x = 0
    if astronaut_rect.x > WIDTH - astronaut_rect.width:
        astronaut_rect.x = WIDTH - astronaut_rect.width


# Define main loop
running = True
clock = pygame.time.Clock()
spaceships = []
max_spaceships = 8  # Maximum number of spaceships allowed on the screen


# Initialize clock object to cap frame rate
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state
    screen.blit(space_background, (0, 0))
    screen.blit(astronaut, astronaut_rect)

    # Create new spaceship randomly if below the max limit
    if len(spaceships) < max_spaceships and random.randint(0, 100) < 2:
        spaceships.append(create_spaceship())

    # Move and draw spaceships
    move_spaceships(spaceships)
    draw_spaceships(spaceships)

    # Handle astronaut movement
    moving()

    # Update display
    pygame.display.flip()
    clock.tick(30)  # Limit frame rate to 30 fps

# Quit Pygame
pygame.quit()
sys.exit()
