import pygame as pg

# game constants
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = (800,600)
CAPTION = 'no name yet'
CONTROLS = {
    pg.K_UP:  "UP",
    pg.K_DOWN: "DOWN",
    pg.K_LEFT:  "LEFT",
    pg.K_RIGHT: "RIGHT"
}
DIR_VECTORS = {
    "UP":  (0, -1),
    "DOWN":  (0, 1),
    "LEFT":  (-1, 0),
    "RIGHT":  (1, 0)
}
DIRECTIONS = ("UP", "LEFT", "DOWN", "RIGHT")

# Initialization
pg.init()
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

gfx_group = pg.sprite.LayeredDirty()

# load resources