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
    game = Game(120, COLOR_WHITE, win, WIDTH, HEIGHT)
    game.start()
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE: 
                    running = False
                if event.key == K_RETURN:
                        game.restart()
            elif event.type == MOUSEBUTTONDOWN and game.get_status() == 0:
                if event.button == 1:
                    game.left_click()
                if event.button == 3:
                    game.right_click()
            elif event.type == pygame.QUIT:
                running = False
        game.update()  
    pygame.quit()

if __name__ == "__main__":
    main()