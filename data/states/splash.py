import pygame as pg

from .. import util, state

class SplashState(state._State):
    def __init__(self):
        super(SplashState, self).__init__()
        self.bg_color = (45,123,145)
        self.duration = 5 #seg

    def update(self, dt, current_time):
        self.duration -= dt
        if self.duration <= 0:
            self.quit = True # must be self.done

    def render(self, surface):
        surface.fill(self.bg_color)


