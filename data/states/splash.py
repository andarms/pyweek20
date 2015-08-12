import pygame as pg

import state
from .. import util

class SplashState(state._State):
    def __init__(self):
        super(SplashState, self).__init__()
        self.bg_color = (0,0,0)
        self.text_color = (155,255,155)
        self.duration = 3 #seg
        self.next = "Game"
        self.title = "HackerMan"
        self.titleSurface = self.make_title_surface()

    def star(self, data, current_time):
        super(SplashState, self).start(data, current_time)
        self.duration = 3

    def make_title_surface(self):
        font = pg.font.Font(util.FONTS['west-england.regular'], 40)
        return font.render(self.title, False, self.text_color)


    def update(self, dt, current_time, keys):
        self.duration -= dt
        if self.duration <= 0 or keys[pg.K_RETURN]:
            self.done = True # must be self.done

    def render(self, surface):
        surface.fill(self.bg_color)
        return surface.blit(self.titleSurface, util.SCREEN_RECT.center)



