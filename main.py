import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (27, 140, 141)
LIGHTGREY = (189, 195, 199)
GREEN = (60, 186, 84)
RED = (219, 50, 54)
YELLOW = (244, 194, 13)
BLUE = (72, 133, 237)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

# Game Loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
