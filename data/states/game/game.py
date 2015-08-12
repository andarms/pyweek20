import pygame as pg

from ... import util, actors, hud
from .. import state
import level

class GameState(state._State):
    def __init__(self):
        super(GameState, self).__init__()
        self.bg_color = (0, 0, 0)
        self.player = self.player = actors.Player([50,50])
        self.level = level.Level(self.player)
        self.hud = hud.HUD()

    def handle_events(self, event):
        self.level.handle_events(event)

    def update(self, dt, current_time, keys):
        self.level.update(dt, current_time, keys)
        self.hud.update(self.player)

    def render(self, surface):
        dirty = []
        surface.fill(self.bg_color)
        rect1 = self.level.render(surface)
        rect2 = self.hud.render(surface)
        dirty.extend((rect1, rect2))
        return dirty
