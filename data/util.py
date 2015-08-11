import os
import pygame as pg

# game constants
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = (800,600)
CAPTION = 'Hackerman'
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
WORLD = [
    "####################################################",
    "#      #                                           #",
    "#                                                  #",
    "#                  ######=####    ###########      #",
    "#      #                                           #",
    "#      #                                           #",
    "#      #                           #######         #",
    "#      #                                           #",
    "#      #                                           #",
    "#      #                            #######        #",
    "#      #                                           #",
    "#      #                                   ####### #",
    "#                                                  #",
    "#                                                  #",
    "#            #########=#######                     #",
    "#                                                  #",
    "#                                                  #",
    "#                                                  #",
    "#    ###################      ######### ############",
    "#                                                  #",
    "#                                                  #",
    "####################################################"
]
WALL_SIZE = 32
CMDS = ('$a%6dgjgk', '55r4/&38r4fefs5', '(gsdkj7*7', '68eq3dea2', '34/(1343', '#12-/|"4')

# Use to show a message in the screen from any object
msg = None

# Helper functions
def load_all_gfx(directory,colorkey=(0,0,0),accept=(".png",".jpg",".bmp")):
    """
    Load all graphics with extensions in the accept argument.  If alpha
    transparency is found in the image the image will be converted using
    convert_alpha().  If no alpha transparency is detected image will be
    converted using convert() and colorkey will be set to colorkey.
    """
    graphics = {}
    for pic in os.listdir(directory):
        name,ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics


def load_all_music(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """
    Create a dictionary of paths to music files in given directory
    if their extensions are in accept.
    """
    songs = {}
    for song in os.listdir(directory):
        name,ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def load_all_fonts(directory, accept=(".ttf",)):
    """
    Create a dictionary of paths to font files in given directory
    if their extensions are in accept.
    """
    return load_all_music(directory, accept)


# Initialization
pg.init()
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

gfx_group = pg.sprite.LayeredDirty()

# load resources
FONTS = load_all_fonts(os.path.join('resources', 'fonts'))