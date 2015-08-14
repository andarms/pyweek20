import pygame as pg

import state
from .. import util

class SplashState(state._State):
    def __init__(self):
        super(SplashState, self).__init__()
        self.bg_color = (0,0,0)
        self.text_color = (155,255,155)
        self.duration = 3 #seg
        self.image = pg.Surface(util.SCREEN_SIZE)
        self.next = "MainMenu"
        self.title = "HackerMan"
        self.titleSurface = self.make_title_surface()

    def start(self, data, current_time):
        super(SplashState, self).start(data, current_time)
        self.duration = 3

    def make_title_surface(self):
        font = pg.font.Font(util.FONTS['west-england.regular'], 40)
        return font.render(self.title, False, self.text_color)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.done = True

    def update(self, dt, current_time, keys):
        self.duration -= dt
        if self.duration <= 0:
            self.done = True

    def render(self, surface):
        self.image.fill(self.bg_color)
        self.image.blit(self.titleSurface, util.SCREEN_RECT.center)
        surface.blit(self.image, (0,0))



