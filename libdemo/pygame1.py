import pygame
import sys
import os
import time

# SDL_NOMOUSE=1 SDL_NOMOUSE=1 python3 pil.py
os.environ["SDL_NOMOUSE"] = "1"

pygame.display.init()

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("test.png")
ballrect = ball.get_rect()

screen.fill(black)
screen.blit(ball, ballrect)
pygame.display.flip()

time.sleep(5)
exit()
