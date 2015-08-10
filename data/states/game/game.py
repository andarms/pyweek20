import pygame as pg

from ... import util
from .. import state
import level

class GameState(state._State):
    def __init__(self):
        super(GameState, self).__init__()
        self.bg_color = (56, 68,145)
        self.level = level.Level()      

    def handle_events(self, event):
    	self.level.handle_events(event)

    def update(self, dt, current_time, keys):
        self.level.update(dt, current_time, keys)

    def render(self, surface):
        surface.fill(self.bg_color)
        self.level.render(surface)
