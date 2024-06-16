"""
Author: CHIARA AGOSTINO
Date: 2024-06
Description: Description of your program here.
"""

import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Window")


# Define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game states
OPENING = 0
PLAYING = 1
GAME_OVER = 2

# Initialize game conditions
player_score = 0
game_state = OPENING

# Initialize more variables and states below

title_screen = pygame.image.load("title_screen.jpeg").convert()
title_screen = pygame.transform.scale(title_screen, (WIDTH, HEIGHT))

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
        astronaut_rect.x -= 10
    if keys[pygame.K_RIGHT]:
        astronaut_rect.x += 10

    if astronaut_rect.x < 0:
        astronaut_rect.x = 0
    if astronaut_rect.x > WIDTH - astronaut_rect.width:
        astronaut_rect.x = WIDTH - astronaut_rect.width


def check_collisions(spaceships, astronaut_rect):
    for spaceship in spaceships:
        if spaceship[0].colliderect(astronaut_rect):
            return True
    return False


def handle_time():
    elapsed_time = time.time() - start_time
    max_spaceships = 5 + int(elapsed_time / 10)


def reset_game():
    global spaceships, astronaut_rect, start_time, max_spaceships, player_score
    spaceships = []
    astronaut_rect.midbottom = (WIDTH // 2, HEIGHT)
    start_time = time.time()
    max_spaceships = 5    
    player_score = 0


# Define main loop
running = True
clock = pygame.time.Clock()
spaceships = []
max_spaceships = 6 
start_time = time.time()
game_state = OPENING

def display_title_screen():
    screen.blit(title_screen, (0,0))
    font = pygame.font.Font(None, 74)
    text = font.render("Press SPACE to start", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
    screen.blit(text, text_rect)
    pygame.display.flip()


def display_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {int(player_score)}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Initialize clock object to cap frame rate

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == OPENING:
        display_title_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = PLAYING
            reset_game()

    elif game_state == PLAYING:
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
    
        handle_time()

        # Update and display score
        elapsed_time = time.time() - start_time
        player_score = elapsed_time 
        display_score(player_score)
    
        #Reset game if astronaut comes into contact with spaceship
        if check_collisions(spaceships, astronaut_rect):
            game_state = GAME_OVER
            final_score = player_score
    

    elif game_state == GAME_OVER:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over!", True, WHITE)
        text_rect = text.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        game_state = OPENING


        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Final Score: {int(final_score)}", True, WHITE)
        score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(score_text, score_text_rect)
                    
                                 


    

 
    

    # Update display
    pygame.display.flip()
    clock.tick(30)  # Limit frame rate to 30 fps

# Quit Pygame
pygame.quit()
sys.exit()
