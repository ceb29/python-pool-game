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
        self.ball_status = 0
        self.background = sprite_classes.Pool_Table(WIDTH, HEIGHT, "pool_images/pool_table_all.png")
        self.border = sprite_classes.Border(WIDTH, HEIGHT, "pool_images/pool_border.png")
        self.pockets = sprite_classes.Pockets(WIDTH, HEIGHT, "pool_images/pool_holes.png")
        self.qball = sprite_classes.QBall(self.width, self.height, (width/2 - 200, height/2+5), 0)
        self.eight_ball = sprite_classes.Eight_Ball(self.width, self.height, (self.width/2 + 200 + 20 * 2, self.height/2), 4)
        self.balls = pygame.sprite.Group()
        self.surfaces = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.clock_speed = clock_speed
        self.win_rgb = rgb_tuple
        self.ball_list = []
        self.flag_list = []
        self.number_balls = 16
        self.stick_speed = 0
        self.balls_in_pocket = 0

    def get_ball_status(self):
        return self.ball_status

    def set_ball_status(self, status):
        self.ball_status = status

    def get_status(self):
        return self.game_status

    def create_flag_list(self):
        number_list_elements = 0
        for i in range (1, self.number_balls):
            number_list_elements += i
        for i in range (number_list_elements):
            self.flag_list.append(0)

    #functions for cleaning up sprites
    def remove_balls(self):
        self.ball_list = []
        for ball in self.balls:
            ball.kill()

    def remove_sprites(self):
        self.remove_balls()
        self.surfaces = pygame.sprite.Group()

    #functions for game progression
    def start(self):
        self.create_flag_list()
        self.add_sprites()

    def restart(self):
        self.remove_sprites()
        self.background.clear()
        self.balls_in_pocket = 0
        self.create_flag_list()
        self.add_sprites()
        self.game_status = 0
    
    def set_all_move_status(self, status):
        for i in range(len(self.ball_list)):
            self.ball_list[i].set_move_status(status)

    def determine_ball_status(self):
        ball_status = 0
        for i in range(len(self.ball_list)):
            if self.ball_list[i].get_speed() > 0:
                ball_status = 1
        if self.ball_status != ball_status:
            self.background.clear()
        self.ball_status = ball_status
        self.set_all_move_status(ball_status)
        
    #draw all surfaces on screen
    def draw_surfaces(self):
        for s in self.surfaces:
            self.win.blit(s.surf1, s.rect)
    
    def draw_stick(self):
        self.background.draw_line(self.qball.get_center(), pygame.mouse.get_pos())
            
    def update_stick_speed(self):
        length = self.background.get_line_length()
        self.stick_speed = length / 10
        if self.stick_speed == 0:
            self.stick_speed = 1
        self.qball_hit()

    def qball_hit(self):
        end_point = self.background.get_line_end_point()
        x = end_point[0] - self.qball.get_center_x()
        y = end_point[1] - self.qball.get_center_y()
        x_sign = self.get_sign(x)
        y_sign = self.get_sign(y)
        if y == 0:
            self.qball.set_speedx(self.stick_speed * x_sign)
        elif x == 0:
            self.qball.set_speedy(self.stick_speed * y_sign)
        else:
            speed = self.stick_speed
            theta = math.atan(abs(y/x))
            new_x = speed * math.cos(theta)
            new_y = speed * math.sin(theta)
            self.qball.set_speedx(round(new_x) * x_sign)
            self.qball.set_speedy(round(new_y) * y_sign)
        
    #update all sprite positions
    def update_sprite_pos(self):
        if self.qball.locked == 0:
            self.qball.change_position_mouse()
        self.balls.update()

    #main game function
    def update(self):
        self.determine_ball_status()
        if self.qball.get_locked() == 1 and self.ball_status == 0:
            self.draw_stick()
        self.win.fill(self.win_rgb)
        self.text.update_text(self.game_status)
        if self.game_status == 0:
            self.draw_surfaces()
            self.update_sprite_pos()
            self.check_for_collisions()
        pygame.display.flip()
        self.clock.tick(self.clock_speed) 
    
    def add_q_and_eight_balls(self):
        self.qball = sprite_classes.QBall(self.width, self.height, (self.width/2 - 200, self.height/2+5), 0)
        self.eight_ball = sprite_classes.Eight_Ball(self.width, self.height, (self.width/2 + 200 + 20 * 2, self.height/2), 4)
        self.balls.add(self.qball)
        self.ball_list.append(self.qball)
        self.surfaces.add(self.qball)
        self.surfaces.add(self.eight_ball)
        self.balls.add(self.eight_ball)
        self.ball_list.append(self.eight_ball)

    def add_numbered_balls(self):
        starting_point = self.width/2 + 200
        width_spacing = 20
        height_spacing = 11
        ball_centers = [(starting_point, self.height/2), #row 1
                        (starting_point + width_spacing, self.height/2 + height_spacing), (starting_point + width_spacing, self.height/2 - height_spacing), #row 2
                        (starting_point + width_spacing * 2, self.height/2 + height_spacing * 2), (starting_point + width_spacing * 2, self.height/2 - height_spacing * 2), #row 3
                        (starting_point + width_spacing * 3, self.height/2 + height_spacing), (starting_point + width_spacing * 3, self.height/2 - height_spacing), (starting_point + width_spacing * 3, self.height/2 + height_spacing * 3), (starting_point + width_spacing * 3, self.height/2 - height_spacing * 3), #row 4
                        (starting_point + width_spacing * 4, self.height/2), (starting_point + width_spacing * 4, self.height/2 + height_spacing * 2), (starting_point + width_spacing * 4, self.height/2 - height_spacing * 2), (starting_point + width_spacing * 4, self.height/2 + height_spacing  * 4), (starting_point + width_spacing * 4, self.height/2 - height_spacing * 4)] #row 5
        random.shuffle(ball_centers)
        for i in range(0, self.number_balls - 2):
            ball = sprite_classes.Balls(self.width, self.height, ball_centers[i], i + 1)
            self.ball_list.append(ball)
            self.balls.add(ball)
            self.surfaces.add(ball)

    def add_balls(self):
        self.add_q_and_eight_balls()
        self.add_numbered_balls()

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
        rand_int1 = random.randint(2, 4)
        rand_int2 = random.randint(2, 4)
        if y == 0:
            y = 0.001
        elif x == 0:
            x = 0.001
        else:
            x_sign = self.get_sign(x)
            y_sign = self.get_sign(y)
            speed = ball1.get_speed()
            theta = math.atan(abs(y/x))
            new_x = speed * math.cos(theta)
            new_y = speed * math.sin(theta)
            ball2.set_speedx(round(new_x) * x_sign)
            ball2.set_speedy(round(new_y) * y_sign)
            ball1.set_speedx(round(ball1.get_speedx()/rand_int1)) #need to figure out what speed should be of faster ball after collision
            ball1.set_speedy(round(ball1.get_speedy()/rand_int2))    

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

    def ball_collisions(self):
        flag_number = 0
        for i in range(self.number_balls):
            for j in range(i+1, self.number_balls):
                self.collision(self.ball_list[i], self.ball_list[j], flag_number)
                flag_number += 1

    def ball_pocket_collisions(self):
        ball_in_pocket = pygame.sprite.spritecollideany(self.pockets, self.balls, collided=pygame.sprite.collide_mask)
        if ball_in_pocket != None:
            self.balls_in_pocket += 1
            ball_in_pocket.set_pocket_status(1)
            ball_in_pocket.set_pocket_number(self.balls_in_pocket)
            
    def check_for_collisions(self):
        self.ball_collisions()
        self.ball_pocket_collisions()

    def left_click(self):
        if self.ball_status == 0:
            if self.qball.get_locked() == 0:
                #lock qball position
                self.qball.set_locked(1)
            elif self.qball.get_locked() == 1:
                #shoot ball
                self.update_stick_speed()

    def right_click(self):
        #place qball with mouse
        if self.ball_status == 0:
            if self.qball.get_locked() == 1:
                self.background.clear()
                self.qball.set_locked(0)
