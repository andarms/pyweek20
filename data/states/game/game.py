import pygame as pg

from ... import util
from .. import state
import level

class GameState(state._State):
    def __init__(self):
        super(GameState, self).__init__()
        self.bg_color = (0, 0, 0)
        self.level = level.Level()      
        self.font = pg.font.Font(util.FONTS['west-england.regular'], 30)

    def handle_events(self, event):
        self.level.handle_events(event)

    def update(self, dt, current_time, keys):
        self.level.update(dt, current_time, keys)

    def render(self, surface):
        dirty = []
        surface.fill(self.bg_color)
        rect1 = self.level.render(surface)
        dirty.extend((rect1))
        if util.msg:
            image = self.font.render(util.msg, False, (255,255,255))
            i_rect = image.get_rect(center=util.SCREEN_RECT.center)
            surface.blit(image, i_rect)
        return dirty
