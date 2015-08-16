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
        self.player = actors.Player((0,0))

    def start(self, data, current_time):
        super(GameState, self).start(data, current_time)
        self.game_over = False
        if self.data:
            self.player = self.data["player"]
        self.level = level.Level(self.player)
        self.hud = hud.HUD()

    def clear(self):
        super(GameState, self).clear()
        self.data['player'] = self.player
        return self.data

    def handle_events(self, event):
        self.player.handle_events(event)

    def update(self, dt, current_time, keys):
        if self.player.hp > 0:
            self.hud.update(self.player)
            if self.level.is_clear():
                self.next = "MissionComplete"
                self.hud.set_message("Level clear")
                if keys[pg.K_RETURN]:
                    self.done = True
            else:
                self.level.update(dt, current_time, keys)
        else:
            self.player.kill()
            self.next = "GameOver"
            self.done = True

    def render(self, surface):
        surface.fill(self.bg_color)
        self.level.render(surface)
        self.hud.render(surface)
