import pygame
import neat
import time
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird():
    IMAGES  = BIRD_IMAGES
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.IMAGE_COUNT = 0
        self.IMAGE = self.IMAGES[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel + self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self, win):
        self.IMAGE_COUNT += 1

        if self.IMAGE_COUNT < self.ANIMATION_TIME:
            self.IMAGE = self.IMAGES[0]
        elif self.IMAGE_COUNT < self.ANIMATION_TIME*2:
            self.IMAGE = self.IMAGES[1]
        elif self.IMAGE_COUNT < self.ANIMATION_TIME*3:
            self.IMAGE = self.IMAGES[2]
        elif self.IMAGE_COUNT < self.ANIMATION_TIME*4:
            self.IMAGE = self.IMAGES[1]
        elif self.IMAGE_COUNT < self.ANIMATION_TIME*4 + 1:
            self.IMAGE = self.IMAGES[0]
            self.IMAGE_COUNT = 0

        if self.tilt <= -80:
            self.IMAGE = self.IMAGES[1]
            self.IMAGE_COUNT = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.IMAGE, self.tilt)
        new_rect = rotated_image.get_rect(center=self.IMAGE.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.IMAGE)


def draw_window(win, bird):
    win.blit(BG_IMAGE, (0, 0))
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run  = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(win, bird)

        bird.move()
    pygame.quit()
    quit()

main()