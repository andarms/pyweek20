import pygame as pg

from ... import util, actors, hud
from .. import state
import level

class GameState(state._State):
    def __init__(self):
        super(GameState, self).__init__()
        self.bg_color = (0,0,0)        
        self.hud = hud.HUD()
        self.game_over = False

    def start(self, data, current_time):
        super(GameState, self).start(data, current_time)
        self.game_over = False
        self.player = self.player = actors.Player([50,50])
        self.level = level.Level(self.player)

    def clear(self):
        self.data['player'] = self.player
        self.player = None
        self.level = None
        return self.data

    def handle_events(self, event):
        self.player.handle_events(event)

    def update(self, dt, current_time, keys):
        if self.player.hp > 0:
            self.level.update(dt, current_time, keys)
            self.hud.update(self.player)
        else:
            self.player.kill()
            self.next = "GameOver"
            self.done = True

    def render(self, surface):
        dirty = []
        surface.fill(self.bg_color)
        rect1 = self.level.render(surface)
        rect2 = self.hud.render(surface)
        dirty.extend((rect1, rect2))
        return dirty
