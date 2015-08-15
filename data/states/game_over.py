import pygame as pg

import state
from .. import util

FONT = pg.font.Font(util.FONTS['west-england.regular'], 70)
SMALL_FONT = pg.font.Font(util.FONTS['west-england.regular'], 40)

class GameOverState(state._State):
    def __init__(self):
        super(GameOverState, self).__init__()
        self.bg_color = (0,0,0)
        self.text_color = (255,255,255)
        self.duration = 3 #seg
        self.image = pg.Surface(util.SCREEN_SIZE)
        self.next = "Splash"
        self.title = "Game Over"
        self.titleSurface = self.make_title_surface()
        self.rect = self.titleSurface.get_rect()
        self.rect.center = util.SCREEN_RECT.center
        self.sprites = pg.sprite.Group()
        self.score = pg.sprite.Sprite(self.sprites)
        self.name_sprite = pg.sprite.Sprite(self.sprites)
        self.name = ""
        self.old_name = None

    def start(self, data, start_time):
        super(GameOverState, self).start(data, start_time)
        self.player = self.data["player"]
        text = "Score: %s" % (self.player.score)
        self.score.image = SMALL_FONT.render(text, False, (255, 255, 255))
        self.score.rect = self.score.image.get_rect()        
        self.score.rect.centerx = self.rect.centerx
        self.score.rect.y = self.rect.bottom + 20
        self.update_name()

    def clear(self):
        self.name = ""

    def make_title_surface(self):
        return FONT.render(self.title, False, self.text_color)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key >= 65 and event.key <= 122:
                self.name += chr(event.key)
            if event.key == pg.K_BACKSPACE:
                self.name = self.name[:-1]
            if event.key == pg.K_RETURN:
                self.done = True

    def update(self, *args):
        if self.name != self.old_name:
            self.update_name()
            self.old_name = self.name

    def update_name(self):
        if len(self.name) <= 7:
            self.name_sprite.image = SMALL_FONT.render(self.name.upper(), False, (255,255,255))
            self.name_sprite.rect = self.image.get_rect()            
            self.name_sprite.rect.x = self.score.rect.x
            self.name_sprite.rect.y = self.score.rect.bottom+20

    def render(self, surface):
        self.image.fill(self.bg_color)
        self.image.blit(self.titleSurface, self.rect)
        self.sprites.draw(self.image)
        surface.blit(self.image, (0,0))