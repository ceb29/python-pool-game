import pygame
import random
import math
import time
from pygame.constants import RLEACCEL #buttons used in game
from constants import COLOR_BLACK, COLOR_WHITE

class Sprites(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, center):
        super(Sprites, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center = center

    def get_center(self):
        return self.center

    def get_center_x(self):
        return self.center[0]

    def get_center_y(self):
        return self.center[1]

    def out_of_bounds(self):
        if self.rect.right > self.screen_width:
            self.rect.move_ip(-self.screen_width, 0)
        if self.rect.left < 0:
            self.rect.move_ip(self.screen_width, 0)
        if self.rect.top < 0:
            self.rect.move_ip(0, self.screen_height)
        if self.rect.bottom > self.screen_height:
            self.rect.move_ip(0, -self.screen_height) 

class Balls(Sprites):
    def __init__(self, screen_width, screen_height, ball_center, ball_number):
        Sprites.__init__(self, screen_width, screen_height, ball_center)
        self.surf1 = pygame.image.load("pool_images/ball" + str(ball_number) + ".png").convert()
        #self.surf1 = pygame.transform.rotate(self.surf1, random.randint(0, 360))
        self.surf1.set_colorkey(COLOR_BLACK, RLEACCEL)
        self.mask = pygame.mask.from_surface(self.surf1)
        self.flag1 = 0
        self.flag2 = 0
        self.speedx = 0
        self.speedy = 0
        self.speed = math.sqrt(self.speedx**2 + self.speedy**2)
        self.rect = self.surf1.get_rect(center = ball_center)
        self.last1 = int(time.time()*1000)
        self.last2 = int(time.time()*1000)
        self.delay1 = 1
        self.delay2 = 100

    def get_speed(self):
        return self.speed

    def get_speedx(self):
        return self.speedx

    def get_speedy(self):
        return self.speedy

    def set_speed(self, speed):
        self.speed = speed

    def set_speedx(self, speedx):
        self.speedx = speedx

    def set_speedy(self,  speedy):
        self.speedy = speedy

    def ball_slow_down(self):
        current1 = int(time.time()*1000)
        if current1 - self.last1 > self.delay1:
            self.bounce1()
            self.bounce2()
            self.last1 = int(time.time()*1000)
        current2 = int(time.time()*1000)
        if current2 - self.last2 > self.delay2:
            self.delay1 += 2
            self.last2 = int(time.time()*1000)
        if self.delay1 > 100 + self.speed * 10:
            self.speedx = 0
            self.speedy = 0

    def update(self):
        self.center = [self.rect.centerx, self.rect.centery]
        self.speed = math.sqrt(self.speedx**2 + self.speedy**2)
        #self.bounce1()
        #self.bounce2()
        self.ball_slow_down()

    def bounce1(self):
        #change position on wall bounces
        self.rect.move_ip(self.speedx , 0)
        if self.rect.right > self.screen_width/2 + 324:
            self.speedx *= -1
        elif self.rect.left < self.screen_width/2 - 324:
            self.speedx *= -1

    def bounce2(self):
        self.rect.move_ip(0, self.speedy )            
        if self.rect.bottom > self.screen_height/2 + 157:
            self.speedy *= -1
        elif self.rect.top < self.screen_height/2 - 159:
            self.speedy *= -1

class QBall(Balls):
    def __init__(self, screen_width, screen_height, center, ball_number):
        Balls.__init__(self, screen_width, screen_height, center, ball_number)
        self.surf1.set_colorkey(COLOR_BLACK, RLEACCEL)
        self.speedx = 10
        self.speedy = 0

class Eight_Ball(Balls):
    def __init__(self, screen_width, screen_height, center, ball_number):
        Balls.__init__(self, screen_width, screen_height, center, ball_number)
        self.surf1 = pygame.image.load("pool_images/ball15.png").convert()
        self.surf1.set_colorkey(COLOR_WHITE, RLEACCEL)

class Background(Sprites):
    def __init__(self, screen_width, screen_height, file_image):
        Sprites.__init__(self, screen_width, screen_height, [screen_width/2,screen_height/2])
        self.surf1 = pygame.image.load(file_image).convert()
        self.surf1.set_colorkey(COLOR_WHITE, RLEACCEL)
        self.mask = pygame.mask.from_surface(self.surf1)
        self.rect = self.surf1.get_rect(center = (self.screen_width/2,self.screen_height/2))

class Border(Background):
    def __init__(self, screen_width, screen_height, file_image):
        Background.__init__(self, screen_width, screen_height, file_image)

class Holes(Background):
    def __init__(self, screen_width, screen_height, file_image):
        Background.__init__(self, screen_width, screen_height, file_image)