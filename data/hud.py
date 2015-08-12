import pygame as pg

import util

FONT = pg.font.Font(util.FONTS['west-england.regular'], 20)
BiG_FONT = pg.font.Font(util.FONTS['west-england.regular'], 50)
WHITE = (255,255,255)
BLACK = (0,0,0)

class HUD(object):
    """docstring for HUD"""
    def __init__(self):
        self.life = LifeStatus()
        self.image = pg.Surface(util.SCREEN_SIZE)
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft=(0,0))
        self.message = None
        self.message_rect = None

    def update(self, player):
        self.life.update(player)

    def set_message(self, msg, des=None):
        self.message = BiG_FONT.render(msg, False, WHITE, BLACK)
        self.message_rect = self.message.get_rect()
        self.message_rect.center = self.rect.center

    def render(self, surface):
        self.life.render(self.image)
        if self.message:
            self.image.blit(self.message, self.message_rect)
        return surface.blit(self.image, self.rect)
        

class LifeStatus(object):
    def __init__(self):
        self.image = pg.Surface((50,50))
        self.rect = self.image.get_rect()        
        self.hp = FONT.render('', False, WHITE)
        self.hp_rect = self.hp.get_rect(center=self.rect.center)

    def update(self, player):
        self.hp = FONT.render(str(player.hp), False, WHITE)
        self.hp_rect = self.hp.get_rect(center=self.rect.center)
        
    def render(self, surface):
        self.image.fill((0,0,0))
        pg.draw.rect(self.image, WHITE, self.rect, 5)
        self.image.blit(self.hp, self.hp_rect)
        surface.blit(self.image, (16,16))

class Tooltip(pg.sprite.Sprite):
    def __init__(self, text, (x, y)):
        super(Tooltip, self).__init__()
        self.text = text
        self.bg = BLACK
        self.fg = WHITE
        self.image = FONT.render(text, False, self.fg, self.bg)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y - 32

    def change_text(self, text):
        if not self.text == text:
            self.text = text
            x, y = self.rect.center
            self.image = FONT.render(text, False, self.fg, self.bg)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y
        