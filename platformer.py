import pygame
from pygame.locals import *

# initialize pygame
pygame.init()

screen_width = 1000
screen_height = 1000

# creates a game window
screen = pygame.display.set_mode((screen_width, screen_height))
# names game window
pygame.display.set_caption('Platformer Game')

# load images

sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')




# keeps window displaying until run is false
run = True
while run:

    # put images onto display
    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (100, 100))

    # checks whether user clicks x to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window with instruction
    pygame.display.update()
pygame.quit()

