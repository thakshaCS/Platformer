import pygame
from pygame.locals import *

# initialize pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60


screen_width = 1000
screen_height = 500 # make 500 to see the guy

# creates a game window
screen = pygame.display.set_mode((screen_width, screen_height),
                                 pygame.RESIZABLE)

# names game window
pygame.display.set_caption('Platformer Game')

# define game variables
tile_size = 50

# load images

sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')


def draw_grid():
    for line in range(0, 20):
        # (255, 255, 255) = colour white
        # (0, line * tile_size) = x, y coord

        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size),
                         (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0),
                         (line * tile_size, screen_height))
class Player():

    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right,(40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_left.append(img_left)
            self.images_right.append(img_right)

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):

        dx = 0
        dy = 0

        walk_cooldown = 5

        #get keypresses
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = - 15
            self.jumped = True

        if key[pygame.K_SPACE] == False:
            self.jumped = False

        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1

        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1

        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0

            if self.direction == 1:
                self.image = self.images_right[self.index]

            if self.direction == -1:
                self.image = self.images_left[self.index]

        # handle animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index == len(self.images_right):
                self.index = 0

            if self.direction == 1:
                self.image = self.images_right[self.index]

            if self.direction == -1:
                self.image = self.images_left[self.index]




        # add gravity
        self.vel_y += 1
        dy += self.vel_y

        # check for collison
        for tile in world.tile_list:

            # check for collision of player
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                

                # check if below the ground from jumping -> negative velocity
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0

                # check if above ground -> falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0




        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        # prevnts player from going off the screen
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        # draw player onto screen
        screen.blit(self.image, self.rect)

class World():
    def __init__(self, data):

        self.tile_list = []
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')

        # go through each tile one by one
        row_count = 0

        for row in data:
            col_count = 0
            for tile in row:

                # tile is dirt
                if tile == 1:
                    # scale it to fit tile
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    # create rectangle from image
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                # tile is grass
                if tile == 2:
                    # scale it to fit tile
                    img = pygame.transform.scale(grass_img,
                                                 (tile_size, tile_size))
                    # create rectangle from image
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100, screen_height - 130)
world = World(world_data)
# keeps window displaying until run is false
run = True
while run:

    # fixes frame rate
    clock.tick(fps)

    # put images onto display
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    world.draw()
    player.update()
    #draw_grid()

    # checks whether user clicks x to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window with instruction
    pygame.display.update()
pygame.quit()
