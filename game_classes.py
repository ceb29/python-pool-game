import pygame
import random
import math
import sprite_classes
from constants import *

class Game_Text():
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.text_list = []
        self.font = pygame.font.Font('freesansbold.ttf', 32) #font used for all text
        self.win = win
        self.game_over_width = (self.width/2) - 100
        self.game_over_height = (self.height/2) - 32

    def create_text(self):
        text_game_over = self.font.render('Game Over', False, COLOR_BLACK)
        self.text_list = [text_game_over]  

    def update_text(self, game_status):
        if game_status != 0:
            self.win.blit(self.text_list[0], (self.game_over_width, self.game_over_height)) #text_game_over

class Game():
    def __init__(self, clock_speed, rgb_tuple, win, width, height):
        self.width = width
        self.height = height
        self.win = win
        self.text = Game_Text(win, width, height)
        self.game_status = 0
        self.background = sprite_classes.Background(WIDTH, HEIGHT, "pool_images/pool_table_all.png")
        self.border = sprite_classes.Border(WIDTH, HEIGHT, "pool_images/pool_border.png")
        self.holes = sprite_classes.Holes(WIDTH, HEIGHT, "pool_images/pool_holes.png")
        self.qball = sprite_classes.QBall(self.width, self.height, (width/2 - 200, height/2+5), 0)
        self.eight_ball = sprite_classes.Eight_Ball(self.width, self.height, (self.width/2 + 200 + 20 * 2, self.height/2), 4)
        self.balls = pygame.sprite.Group()
        self.surfaces = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.clock_speed = clock_speed
        self.win_rgb = rgb_tuple
        self.ball_list = []
        self.flag_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def get_status(self):
        return self.game_status

    #functions for game progression
    def start(self):
        self.text.create_text()
        self.add_sprites()

    def next_level(self):
        self.surfaces = pygame.sprite.Group()
        self.add_sprites()

    def restart(self):
        self.add_sprites()
        self.game_status = 0

    #draw all surfaces on screen
    def draw_surfaces(self):
        for s in self.surfaces:
            self.win.blit(s.surf1, s.rect)
    
    #update all sprite positions if 
    def update_sprite_pos(self):
        self.balls.update()

    #main game function
    def update(self):
        self.win.fill(self.win_rgb)
        self.text.update_text(self.game_status)
        if self.game_status == 0:
            self.draw_surfaces()
            self.update_sprite_pos()
            self.check_for_collisions()
        #else:
            #self.remove_sprites()
        pygame.display.flip()
        self.clock.tick(self.clock_speed) 
    
    def add_balls(self):
        starting_point = self.width/2 + 200
        width_spacing = 20
        height_spacing = 11
        # ball_centers = [(starting_point, self.height/2), #row 1
        #                 (starting_point + width_spacing, self.height/2 + 11), (starting_point + width_spacing, self.height/2 - height_spacing), #row 2
        #                 (starting_point + width_spacing * 2, self.height/2 + height_spacing * 2), (starting_point + width_spacing * 2, self.height/2 - height_spacing * 2), #row 3
        #                 (starting_point + width_spacing * 3, self.height/2 + height_spacing), (starting_point + width_spacing * 3, self.height/2 - height_spacing), (starting_point + width_spacing * 3, self.height/2 + height_spacing * 3), (starting_point + width_spacing * 3, self.height/2 - height_spacing * 3), #row 4
        #                 (starting_point + width_spacing * 4, self.height/2), (starting_point + width_spacing * 4, self.height/2 + height_spacing * 2), (starting_point + width_spacing * 4, self.height/2 - height_spacing * 2), (starting_point + width_spacing * 4, self.height/2 + height_spacing  * 4), (starting_point + width_spacing * 4, self.height/2 - height_spacing * 4)] #row 5
        # random.shuffle(ball_centers)
        ball_centers = [(starting_point, self.height/2), (starting_point + width_spacing, self.height/2 + 11)]
        self.balls.add(self.qball)
        self.ball_list.append(self.qball)
        self.surfaces.add(self.qball)
        self.surfaces.add(self.eight_ball)
        self.balls.add(self.eight_ball)
        self.ball_list.append(self.eight_ball)
        for i in range(len(ball_centers)):
            ball = sprite_classes.Balls(self.width, self.height, ball_centers[i], i + 1)
            self.ball_list.append(ball)
            self.balls.add(ball)
            self.surfaces.add(ball)

    def add_sprites(self):
        self.surfaces.add(self.background)
        self.add_balls()
    
    def get_sign(self, n):
        n_sign = 1
        if n < 0:
            n_sign = -1
        return n_sign
    
    def collision_speed(self, ball1, ball2):
        #get new speed x and y based off ball1 and ball2 initial speed and collision point
        x = ball2.get_center_x() - ball1.get_center_x()
        y = ball2.get_center_y() - ball1.get_center_y()
        if y == 0:
            speed = ball1.get_speedx()
            ball1.set_speedx(ball2.get_speedx())
            ball2.set_speedx(round(speed/random.randint(1, 4)))
        elif x == 0:
            speed = ball1.get_speedy()
            ball1.set_speedy(ball2.get_speedy())
            ball2.set_speedy(round(speed/random.randint(1, 4))) 
        else:
            x_sign = self.get_sign(x)
            y_sign = self.get_sign(y)
            speed = ball1.get_speed()
            ratio = abs(x / y)
            y_sqr_constant = ratio**2 + 1
            y_sqr = (speed**2)/y_sqr_constant
            new_y = math.sqrt(y_sqr)
            new_x = ratio * new_y
            ball2.set_speedx(round(new_x) * x_sign)
            ball2.set_speedy(round(new_y) * y_sign)
            ball1.set_speedx(round(ball1.get_speedx()/random.randint(1, 4))) #need to figure out what speed should be of faster ball after collision
            ball1.set_speedy(round(ball1.get_speedy()/random.randint(1, 4)))

    def collision(self, ball1, ball2, flag_index):
        collision_coord = pygame.sprite.collide_mask(ball1, ball2)
        if collision_coord != None and self.flag_list[flag_index] == 0:
            if ball1.get_speed() > ball2.get_speed():
                self.collision_speed(ball1, ball2)
            else:
                self.collision_speed(ball2, ball1)
            self.flag_list[flag_index] = 1
        elif collision_coord == None:
            self.flag_list[flag_index] = 0

    def collisions_qball(self, total_balls):
        for i in range(0, total_balls - 1):
            self.collision(self.ball_list[0], self.ball_list[i+1], i)
    
    def collisions_eight_ball(self, total_balls):
        ball_number = 1
        for i in range(ball_number, total_balls - 1):
            list_index = total_balls - 2 + i
            self.collision(self.ball_list[ball_number], self.ball_list[i+1], list_index)

    def collision_ball2(self, total_balls):
        ball_number = 2
        for i in range(ball_number, total_balls - 1):
            list_index = total_balls - 1 + i
            self.collision(self.ball_list[ball_number], self.ball_list[i+1], list_index)

    def ball_collisions(self):
        self.collisions_qball(4)
        self.collisions_eight_ball(4)
        self.collision_ball2(4)

    def check_for_collisions(self):
        self.ball_collisions()

    #functions for cleaning up sprites
    def remove_enemies(self):
        for en in self.enemies:
            en.kill()

    def remove_sprites(self):
        self.player1.kill()
        self.remove_enemies()
        self.surfaces = pygame.sprite.Group()
