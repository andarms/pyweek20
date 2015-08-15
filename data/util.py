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
DIRECTIONS = ("UP", "DOWN", "LEFT", "RIGHT")
reverse_dirs = ("RIGHT","LEFT", "DOWN", "UP" )
ATTACK_KEYS = {
    pg.K_w:  "UP",
    pg.K_s: "DOWN",
    pg.K_a:  "LEFT",
    pg.K_d: "RIGHT"
}
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
    "#      #                                   ###=### #",
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

def split_sheet(sheet, size, columns, rows):
    """
    Divide a loaded sprite sheet into subsurfaces.
    
    The argument size is the width and height of each frame (w,h)
    columns and rows are the integer number of cells horizontally and
    vertically.
    """
    subsurfaces = []
    for y in range(rows):
        row = []
        for x in range(columns): 
            rect = pg.Rect((x*size[0], y*size[1]), size)
            row.append(sheet.subsurface(rect))
        subsurfaces.append(row)
    return subsurfaces


# Initialization
pg.init()
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

os.environ['SDL_VIDEO_CENTERED'] = '1'
gfx_group = pg.sprite.Group()
bullets_group = pg.sprite.Group()

# load resources
FONTS = load_all_fonts(os.path.join('resources', 'fonts'))
GFX = load_all_gfx("resources")
