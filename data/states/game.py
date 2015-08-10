import pygame as pg

from .. import util, state, actors

class GameState(state._State):
    def __init__(self):
        super(GameState, self).__init__()
        self.bg_color = (56, 68,145)
        self.all_sprites = pg.sprite.Group()
        self.player = actors.Player([0,0], self.all_sprites)

    def handle_events(self, event):
    	self.player.handle_events(event)

    def update(self, dt, current_time, keys):    	
        self.all_sprites.update(dt, keys)
        util.gfx_group.update(dt)

    def render(self, surface):
        surface.fill(self.bg_color)
        self.all_sprites.draw(surface)
        util.gfx_group.draw(surface)