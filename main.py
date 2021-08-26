#pool game
#game to learn pygame and practice using classes in python

import pygame
from game_classes import Game
from pygame.constants import K_RETURN, MOUSEBUTTONDOWN, K_ESCAPE, KEYDOWN #buttons used in game
from constants import *

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT)) #creates a game window with given size 

def main():
    running = True
    pygame.mouse.set_visible(False)
    game = Game(30, COLOR_WHITE, win, WIDTH, HEIGHT)
    game.start()
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE: 
                    running = False
                if event.key == K_RETURN and game.get_status() == 1:
                        game.restart()
            elif event.type == MOUSEBUTTONDOWN and game.get_status() == 0: #update orientation or fire projectile
                button_pressed = event.button
               # game.player1.change_front(button_pressed)
                #if event.button == 1:
            elif event.type == pygame.QUIT:
                running = False
        game.update()  
    pygame.quit()

if __name__ == "__main__":
    main()