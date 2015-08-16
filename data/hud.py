import pygame as pg

import util

FONT = pg.font.Font(util.FONTS['west-england.regular'], 20)
BiG_FONT = pg.font.Font(util.FONTS['west-england.regular'], 50)
WHITE = (255,255,255)
BLACK = (0,0,0)

class HUD(object):
    """docstring for HUD"""
    def __init__(self):
        self.image = pg.Surface(util.SCREEN_SIZE)
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft=(0,0))
        self.life = LifeStatus()
        self.score = Score((self.rect.right - 16, 16))
        self.message = None
        self.message_rect = None
        self.infecteds = None

    def update(self, player, level):
        self.life.update(player)
        self.score.update(player)
        self.make_label(level)

    def set_message(self, msg, des=None):
        self.message = BiG_FONT.render(msg, False, WHITE, BLACK)
        self.message_rect = self.message.get_rect()
        self.message_rect.center = self.rect.center

    def make_label(self, level):
        if self.infecteds != len(level.actions):
            self.infecteds = len(level.actions)
            self.info = FONT.render("infected data: %d" % (self.infecteds), False, WHITE)
            pos = (self.rect.right-16, self.score.rect.bottom + 16)
            self.info_rect = self.info.get_rect(topright=pos)

    def render(self, surface):
        self.life.render(surface)
        self.score.render(surface)
        if self.message:
            self.image.blit(self.message, self.message_rect)
        if self.infecteds:
            surface.blit(self.info, self.info_rect)
        surface.blit(self.image, self.rect)
        

class LifeStatus(object):
    def __init__(self):
        self.image = pg.Surface((50,50))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha()    
        self.hp = FONT.render('', False, WHITE)
        self.hp_rect = self.hp.get_rect(center=self.rect.center)
        self.value = 0

    def update(self, player):
        if player.hp != self.value:
            self.value = player.hp
            self.hp = FONT.render(str(self.value), False, WHITE)
            self.hp_rect = self.hp.get_rect(center=self.rect.center)
        
    def render(self, surface):
        self.image.fill((0,0,0))
        pg.draw.rect(self.image, WHITE, self.rect, 5)
        self.image.blit(self.hp, self.hp_rect)
        surface.blit(self.image, (16,16))

class Score(object):
    def __init__(self, pos):
        self.value = 0
        self.image = self.set_score(self.value)
        self.rect = self.image.get_rect(topright=pos)

    def update(self, player):
        if player.score != self.value:
            self.value = player.score
            self.image = self.set_score(self.value)
            self.rect = self.image.get_rect(topright=self.rect.topright)

    def set_score(self, value):
        return BiG_FONT.render(str(value), False, (255,255,0))


    def render(self, surface):
        surface.blit(self.image, self.rect)


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

class FloatingLabel(pg.sprite.Sprite):
    def __init__(self, pos, value, color):
        super(FloatingLabel, self).__init__(util.gfx_group)
        self.image = FONT.render(str(value), False, color)
        self.rect = self.image.get_rect(topleft=pos)
        self.duration = 1 #seg

    def update(self, dt):
        self.duration -= dt
        if self.duration <= 0:
            self.kill()
        else:
            self.rect.y -= 100*dt

class DamageLabel(FloatingLabel):
    def __init__(self, pos, value):
        color = (255,50,50)
        super(DamageLabel, self).__init__(pos, -value, color)

class KillLabel(FloatingLabel):
    def __init__(self, pos, value):
        color = (255,255,50)
        super(KillLabel, self).__init__(pos, value, color)

class SuccessLabel(FloatingLabel):
    def __init__(self, pos, value):
        color = (50,255,50)
        super(SuccessLabel, self).__init__(pos, value, color)
        
        

        
        