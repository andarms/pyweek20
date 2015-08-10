import random
import pygame as pg

from ... import util, actors
from .. import state

class GameState(state._State):
    def __init__(self):
        super(GameState, self).__init__()
        self.bg_color = (56, 68,145)
        self.max_enemies = 7
        self.all_sprites = pg.sprite.LayeredDirty()
        self.enemies = self.make_enemies()
        self.player_singleton = pg.sprite.GroupSingle()
        self.player = actors.Player([0,0], self.player_singleton, self.all_sprites)

    def make_enemies(self):
    	enemies = pg.sprite.LayeredDirty()
    	while len(enemies) < self.max_enemies:
    		x = random.randint(0, util.SCREEN_WIDTH)
    		y = random.randint(0, util.SCREEN_HEIGHT)
    		actors.Bug((x, y), enemies, self.all_sprites)
    	return enemies

    def handle_events(self, event):
    	self.player.handle_events(event)

    def update(self, dt, current_time, keys):    	
        self.player_singleton.update(dt, keys, self.enemies)
        self.enemies.update(dt, current_time)
        util.gfx_group.update(dt)

        for sprite in self.all_sprites:
        	self.all_sprites.change_layer(sprite, sprite.rect.bottom)

    def render(self, surface):
        surface.fill(self.bg_color)
        util.gfx_group.draw(surface)
        self.all_sprites.draw(surface)
