import pygame as pg

import util

FONT = pg.font.Font(util.FONTS['west-england.regular'], 20)
class HUD(object):
    """docstring for HUD"""
    def __init__(self):
        self.life = LifeStatus()
        self.image = pg.Surface(util.SCREEN_SIZE)
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft=(0,0))

    def update(self, player):
        self.life.update(player)

    def render(self, surface):
        self.life.render(self.image)
        return surface.blit(self.image, self.rect)
        

class LifeStatus(object):
    def __init__(self):
        self.image = pg.Surface((50,50))
        self.rect = self.image.get_rect()        
        self.hp = FONT.render('', False, (255,255,255))
        self.hp_rect = self.hp.get_rect(center=self.rect.center)

    def update(self, player):
        self.hp = FONT.render(str(player.hp), False, (255,255,255))
        self.hp_rect = self.hp.get_rect(center=self.rect.center)
        
    def render(self, surface):
        self.image.fill((0,0,0))
        pg.draw.rect(self.image, (255,255,255), self.rect, 5)
        self.image.blit(self.hp, self.hp_rect)
        surface.blit(self.image, (16,16))

class Tooltip(pg.sprite.Sprite):
    def __init__(self, text, (x, y)):
        super(Tooltip, self).__init__()
        self.text = text
        self.image = FONT.render(text, False, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y - 32

    def change_text(self, text):
        if not self.text == text:
            self.text = text
            x, y = self.rect.center
            self.image = FONT.render(text, False, (255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y
        