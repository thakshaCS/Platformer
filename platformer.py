import pygame
from pygame.locals import *

# initialize pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000  # make 500 to see the guy

# creates a game window
screen = pygame.display.set_mode((screen_width, screen_height),
                                 pygame.RESIZABLE)

# names game window
pygame.display.set_caption('Platformer Game')

# define game variables
tile_size = 50
game_over = 0

# load images

sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')
winner_img = pygame.image.load('img/winner.png')
restart_img = pygame.image.load('img/restart_btn.png')


def draw_grid():
    for line in range(0, 20):
        # (255, 255, 255) = colour white
        # (0, line * tile_size) = x, y coord

        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size),
                         (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0),
                         (line * tile_size, screen_height))

class Button():

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        # check mouse over and clicked condition
        if self.rect.collidepoint(pos):
            # ensures clicked accounted once
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        screen.blit(self.image, self.rect)
        return action


class Player():

    def __init__(self, x, y):
       self.reset(x, y)

    def update(self, game_over):

        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:

            # get keypresses
            key = pygame.key.get_pressed()

            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = - 15
                self.jumped = True

            if key[pygame.K_SPACE] == False and self.in_air == False:
                self.jumped = False

            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1

            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1

            # animation of player walking
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

            self.in_air = True

            # check for collision with blocks
            for tile in world.tile_list:

                # check for collision of player in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width,
                                       self.height):
                    dx = 0

                # check for collision of player in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width,
                                       self.height):

                    # check if below the ground from jumping -> negative velocity
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0

                    # check if above ground -> falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        # he landed on something
                        self.in_air = False

            # check for collision with enemies
            if pygame.sprite.spritecollide(self,blob_group,False):
                game_over = -1

            # check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            # check collison with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                # player has won!
                game_over = 1


            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        # draw player onto screen
        screen.blit(self.image, self.rect)
        return game_over

    def reset(self,x,y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_left.append(img_left)
            self.images_right.append(img_right)
        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


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
                    img = pygame.transform.scale(dirt_img,
                                                 (tile_size, tile_size))
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

                if tile == 3:
                    blob = Enemy(col_count * tile_size,
                                 row_count * tile_size + 15)
                    blob_group.add(blob)

                if tile == 6:
                    lava = Lava(col_count * tile_size,
                                row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)

                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1

        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Lava(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

class Exit(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 2, 0, 0, 0, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 6, 6, 2, 5, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 7, 0, 7, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100, screen_height - 130)
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
world = World(world_data)

# create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 - 100, restart_img)
# keeps window displaying until run is false
run = True
while run:

    # fixes frame rate
    clock.tick(fps)

    # put images onto display
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if game_over == 0:
        blob_group.update()

    blob_group.draw(screen)
    lava_group.draw(screen)
    exit_group.draw(screen)

    world.draw()
    game_over = player.update(game_over)

    # player has died
    if game_over == -1:
        if restart_button.draw():
            game_over = 0
            player.reset(100, screen_height - 130)

    # check player has won
    if game_over == 1:
        winner_img_small = pygame.transform.scale(winner_img,(tile_size * 3, tile_size * 2))
        screen.blit( winner_img_small, (screen_width // 2 - 50, screen_height // 2 - 100))




    # draw_grid()

    # checks whether user clicks x to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window with instruction
    pygame.display.update()
pygame.quit()
