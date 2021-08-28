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
        self.ball_number = ball_number
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
        self.move_status = 0
        self.pocket_status = 0
        self.pocket_number = 0

    def get_speed(self):
        return self.speed

    def get_speedx(self):
        return self.speedx

    def get_speedy(self):
        return self.speedy

    def get_delay1(self):
        return self.delay1

    def set_speed(self, speed):
        self.speed = speed

    def set_speedx(self, speedx):
        self.speedx = speedx

    def set_speedy(self,  speedy):
        self.speedy = speedy

    def set_delay1(self, delay):
        self.delay1 = delay

    def set_move_status(self, status):
        self.move_status = status

    def set_pocket_status(self, status):
        self.pocket_status = status

    def set_pocket_number(self, number):
        self.pocket_number = number

    def move_ball(self):
        self.rect.move_ip(self.speedx , 0)
        self.rect.move_ip(0, self.speedy)  

    def ball_slow_down(self):
        current1 = int(time.time()*1000)
        if current1 - self.last1 > self.delay1:
            self.move_ball()
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
        if self.pocket_status == 0:
            if self.move_status == 1:
                self.ball_slow_down()
            else:
                self.delay1 = 1
            self.center = [self.rect.centerx, self.rect.centery]
            self.speed = math.sqrt(self.speedx**2 + self.speedy**2)
        else:
            self.speed = 0
            self.speedx = 0
            self.speedy = 0
            self.center = (20, self.pocket_number * 25)
            self.rect = self.surf1.get_rect(center = self.center)

    def bounce1(self):
        #change position on wall bounces
        if self.rect.right > self.screen_width/2 + 324:
            self.speedx *= -1
        elif self.rect.left < self.screen_width/2 - 324:
            self.speedx *= -1

    def bounce2(self):          
        if self.rect.bottom > self.screen_height/2 + 157:
            self.speedy *= -1
        elif self.rect.top < self.screen_height/2 - 159:
            self.speedy *= -1

class QBall(Balls):
    def __init__(self, screen_width, screen_height, center, ball_number):
        Balls.__init__(self, screen_width, screen_height, center, ball_number)
        self.surf1.set_colorkey(COLOR_BLACK, RLEACCEL)
        self.speedx = 0
        self.speedy = 0
        self.locked = 0
        self.position = 0

    def get_locked(self):
        return self.locked
    
    def set_locked(self, lock):
        self.locked = lock

    def change_position_mouse(self):
        if self.locked == 0:
            self.pocket_status = 0
            #updates the position of player sprite based off of mouse cursor location
            self.position = pygame.mouse.get_pos()
            #if self.position[0] > self.player_size-25 and self.position[0] < 475 and self.position[1] < 475 and self.position[1] > 22: #only update mouse postion if inside window
            self.rect.center = pygame.mouse.get_pos() 

class Eight_Ball(Balls):
    def __init__(self, screen_width, screen_height, center, ball_number):
        Balls.__init__(self, screen_width, screen_height, center, ball_number)
        self.surf1 = pygame.image.load("pool_images/ball15.png").convert()
        self.surf1.set_colorkey(COLOR_WHITE, RLEACCEL)

class QBall_line(Sprites):
    def __init__(self, screen_width, screen_height, center):
        Sprites.__init__(self, screen_width, screen_height, center)


class Background(Sprites):
    def __init__(self, screen_width, screen_height, file_image):
        Sprites.__init__(self, screen_width, screen_height, [screen_width/2,screen_height/2])
        self.file_image = file_image
        self.surf1 = pygame.image.load(file_image).convert()
        self.surf1.set_colorkey(COLOR_WHITE, RLEACCEL)
        self.mask = pygame.mask.from_surface(self.surf1)
        self.rect = self.surf1.get_rect(center = (self.screen_width/2,self.screen_height/2))

    
class Pool_Table(Background):
    def __init__(self, screen_width, screen_height, file_image):
        Background.__init__(self, screen_width, screen_height, file_image)
        self.line_length = 0
        self.position = 0
        self.last_time = int(time.time()*1000)
        self.delay = 1000
        self.line_end_point = [0, 0]

    def get_line_length(self):
        return self.line_length

    def get_line_end_point(self):
        return self.line_end_point

    def clear(self):
        self.surf1 = pygame.image.load(self.file_image).convert()
        self.surf1.set_colorkey(COLOR_WHITE, RLEACCEL)

    def reverse_and_mult(self, start, end, multiple):
        if end[0] > start[0]:
            reversed_endx =  start[0] - multiple * (end[0] - start[0])
        else:
            reversed_endx =  start[0] + multiple * (start[0] - end[0])
        if end[1] > start[1]:
            reversed_endy =  start[1] - multiple * (end[1] - start[1])
        else:
            reversed_endy =  start[1] + multiple * (start[1] - end[1])
        reversed_end = (reversed_endx, reversed_endy)
        return reversed_end

    def calculate_length(self, start, end):
        length_x = end[0] - start[0]
        length_y = end[1] - start[1]
        line_length = math.sqrt(length_x**2 + length_y**2)
        return line_length

    def update_line_length(self, start, end):
        #update line length used for speed calculation
        line_length = self.calculate_length(start, end)
        if line_length <= 150:
            self.line_length = line_length

    def change_radius(self, start, end, new_radius):
        #change end point based off new radius using the known angle
        x = end[0] - start[0]
        y = end[1] - start[1]
        if x == 0:
            if y > 0:
                theta = math.pi/2
            else:
                theta = -math.pi/2
        else:
            theta = math.atan(y / x)
        new_x = new_radius * math.cos(theta)
        new_y = new_radius * math.sin(theta)
        #this is a quick fix
        if x < 0:
            new_end = (-new_x + start[0], -new_y + start[1])  
        else:
            new_end = (new_x + start[0], new_y + start[1])  
        return new_end

    def draw_line(self, start, end):
        self.update_line_length(start, end)
        if self.position != end:
            self.clear()
        new_end = self.reverse_and_mult(start, end, 2) #reverse and double
        new_length = self.calculate_length(start, new_end)
        if new_length > 150:
          new_end = self.change_radius(start, new_end, 150)
        pygame.draw.line(self.surf1 , COLOR_BLACK, start, new_end, 3) 
        self.line_end_point = [new_end[0], new_end[1]] 
        self.position = end

class Border(Background):
    def __init__(self, screen_width, screen_height, file_image):
        Background.__init__(self, screen_width, screen_height, file_image)

class Holes(Background):
    def __init__(self, screen_width, screen_height, file_image):
        Background.__init__(self, screen_width, screen_height, file_image)