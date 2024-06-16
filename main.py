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

# Load images
title_screen = pygame.image.load("title_screen.jpeg").convert()
title_screen = pygame.transform.scale(title_screen, (WIDTH, HEIGHT))

space_background = pygame.image.load("spacebackground.jpeg").convert()
space_background = pygame.transform.scale(space_background, (WIDTH, HEIGHT))

astronaut = pygame.image.load("sprite_1.png").convert_alpha()
astronaut_rect = astronaut.get_rect()
astronaut_rect.midbottom = (WIDTH // 2, HEIGHT)

spaceship_img = pygame.image.load("spaceship-3.png").convert_alpha()

# Initialize variables
spaceships = []
max_spaceships = 5  # Initial maximum number of spaceships
start_time = time.time()
final_score = 0

def create_spaceship():
    """
    Create a spaceship at a random horizontal position at the top of the screen.
  
    Returns:
        tuple: A tuple containing the rectangle for the spaceship's position and the spaceship image.
    """
    x = random.randint(0, WIDTH - spaceship_img.get_width())
    y = -spaceship_img.get_height()
    rect = pygame.Rect(x, y, spaceship_img.get_width(), spaceship_img.get_height())
    return rect, spaceship_img

def move_spaceships(spaceships):
    """
    Move the spaceships down the screen. If a spaceship goes off the screen,
    it is repositioned at the top.
  
    Parameters:
        spaceships (list): List of tuples containing the rectangles and images of the spaceships.
    """
    for spaceship in spaceships:
        spaceship[0].y += 8
        if spaceship[0].top > HEIGHT:
            spaceship[0].x = random.randint(0, WIDTH - spaceship_img.get_width())
            spaceship[0].y = -spaceship_img.get_height()

def draw_spaceships(spaceships):
    """
    Draw the spaceships on the screen.
  
    Parameters:
        spaceships (list): List of tuples containing the rectangles and images of the spaceships.
    """
    for spaceship in spaceships:
        screen.blit(spaceship[1], spaceship[0])

def moving():
    """
    Move the astronaut left or right based on user input.
    """
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
    """
    Check if any spaceship collides with the astronaut.
  
    Parameters:
        spaceships (list): List of tuples containing the rectangles and images of the spaceships.
        astronaut_rect (pygame.Rect): The rectangle representing the astronaut's position.
  
    Returns:
        bool: True if a collision is detected, False otherwise.
    """
    for spaceship in spaceships:
        if spaceship[0].colliderect(astronaut_rect):
            return True
    return False

def reset_game():
    """
    Reset the game state, including the position of the astronaut, clearing spaceships, and resetting
    the score and start time.
    """
    global spaceships, astronaut_rect, start_time, max_spaceships, player_score
    spaceships = []
    astronaut_rect.midbottom = (WIDTH // 2, HEIGHT)
    start_time = time.time()
    max_spaceships = 5   
    player_score = 0

def display_title_screen():
    """
    Display the title screen with the message to press SPACE to start.
    """
    screen.blit(title_screen, (0,0))
    font = pygame.font.Font(None, 74)
    text = font.render("Press SPACE to start", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
    screen.blit(text, text_rect)
    pygame.display.flip()

def display_score(score):
    """
    Display the current score on the screen.
  
    Parameters:
        score (float): The current score to be displayed.
    """
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {int(player_score)}", True, WHITE)
    screen.blit(score_text, (10, 10))

def handle_opening():
    """
    Handle the game state when the game is in the opening state.
    """
    display_title_screen()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        global game_state
        game_state = PLAYING
        reset_game()

def handle_playing():
    """
    Handle the game state when the game is in the playing state.
    """
    global game_state, final_score, player_score, max_spaceships

    # Update game state
    screen.blit(space_background, (0, 0))
    screen.blit(astronaut, astronaut_rect)

    # Increase the max number of spaceships over time
    elapsed_time = time.time() - start_time
    max_spaceships = 5 + int(elapsed_time / 10)  # Increase the number of spaceships every 10 seconds

    # Create new spaceship randomly if below the max limit
    if len(spaceships) < max_spaceships and random.randint(0, 100) < 2:
        spaceships.append(create_spaceship())

    # Move and draw spaceships
    move_spaceships(spaceships)
    draw_spaceships(spaceships)

    # Handle astronaut movement
    moving()

    # Update and display score
    player_score = elapsed_time
    display_score(player_score)

    # Check for collision and reset game if collision detected
    if check_collisions(spaceships, astronaut_rect):
        game_state = GAME_OVER
        final_score = player_score


def handle_game_over():
    """
    Handle the game state when the game is in the game over state.
    """
    global game_state
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Final Score: {int(final_score)}", True, WHITE)
    score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(score_text, score_text_rect)

    pygame.display.flip()
    pygame.time.wait(2000)
    game_state = OPENING


# Define main loop
running = True
clock = pygame.time.Clock()
game_state = OPENING  # Initial game state

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == OPENING:
        handle_opening()
    elif game_state == PLAYING:
        handle_playing()
    elif game_state == GAME_OVER:
        handle_game_over()

    # Update display
    pygame.display.flip()
    clock.tick(30)  # Limit frame rate to 30 fps

# Quit Pygame
pygame.quit()
sys.exit()
