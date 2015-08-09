import pygame as pg

# game constants
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = (800,600)
CAPTION = 'no name yet'

# Initialization
pg.init()
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

# load resources