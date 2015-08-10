import pygame as pg

import state
from .. import util

class SplashState(state._State):
    def __init__(self):
        super(SplashState, self).__init__()
        self.bg_color = (45,123,145)
        self.duration = 3 #seg
        self.next = "Game"

    def update(self, dt, current_time, keys):
        self.duration -= dt
        if self.duration <= 0 or keys[pg.K_RETURN]:
            self.done = True # must be self.done

    def render(self, surface):
        return surface.fill(self.bg_color)


