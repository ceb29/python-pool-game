import pygame
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
        self.qball = sprite_classes.QBall(self.width, self.height, (width/2 - 200, height/2))
        self.balls = pygame.sprite.Group()
        self.surfaces = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.clock_speed = clock_speed
        self.win_rgb = rgb_tuple

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
        ball_centers = [(starting_point, self.height/2), #row 1
                        (starting_point + width_spacing, self.height/2 + 11), (starting_point + width_spacing, self.height/2 - height_spacing), #row 2
                        (starting_point + width_spacing * 2, self.height/2), (starting_point + width_spacing * 2, self.height/2 + height_spacing * 2), (starting_point + width_spacing * 2, self.height/2 - height_spacing * 2), #row 3
                        (starting_point + width_spacing * 3, self.height/2 + height_spacing), (starting_point + width_spacing * 3, self.height/2 - height_spacing), (starting_point + width_spacing * 3, self.height/2 + height_spacing * 3), (starting_point + width_spacing * 3, self.height/2 - height_spacing * 3), #row 4
                        (starting_point + width_spacing * 4, self.height/2), (starting_point + width_spacing * 4, self.height/2 + height_spacing * 2), (starting_point + width_spacing * 4, self.height/2 - height_spacing * 2), (starting_point + width_spacing * 4, self.height/2 + height_spacing  * 4), (starting_point + width_spacing * 4, self.height/2 - height_spacing * 4)] #row 5

        for i in range(len(ball_centers)):
            ball = sprite_classes.Balls(self.width, self.height, ball_centers[i])
            self.balls.add(ball)
            self.surfaces.add(ball)
        self.balls.add(self.qball)
        self.surfaces.add(self.qball)

    def add_sprites(self):
        self.surfaces.add(self.background)
        self.add_balls()
            
    def ball_collisions(self):
        for ball in self.balls:
            x = pygame.sprite.spritecollideany(ball, self.balls, collided = pygame.sprite.collide_mask)
            if x != None and x != ball:
                #print(x.mask.overlap(ball.mask, (5, 5)))
                if ball.speedx > x.speedx:
                    speed = x.speedx
                    x.speedx = ball.speedx
                    ball.speedx /= 2
                else:
                    speed = ball.speedx
                    ball.speedx = x.speedx
                    x.speedx /= 2

                if ball.speedy > x.speedy:
                    speed = x.speedy
                    x.speedy = ball.speedy
                    ball.speedy /= 2
                else:
                    speed = ball.speedy
                    ball.speedy = x.speedy
                    x.speedy /= 2
                

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
