import random
import pygame as pg

from ... import util, actors

WORLD = [
    "####################################################",
    "#      #                                           #",
    "#                                                  #",
    "#                  ###########    ###########      #",
    "#      #                                           #",
    "#      #                                           #",
    "#      #                           #######         #",
    "#      #                                           #",
    "#      #                                           #",
    "#      #                            #######        #",
    "#      #                                           #",
    "#      #                                   ####### #",
    "#                                                  #",
    "#                                                  #",
    "#            #################                     #",
    "#                                                  #",
    "#                                                  #",
    "#                                                  #",
    "#    ###################      ######### ############",
    "#                                                  #",
    "#                                                  #",
    "####################################################"
]
WALL_SIZE = 32
class Level(object):
    """docstring for Level"""
    def __init__(self):     
        self.max_enemies = 7
        self.all_sprites = pg.sprite.LayeredDirty()
        self.walls = self.make_walls()
        self.enemies = self.make_enemies()
        self.player_singleton = pg.sprite.GroupSingle()
        self.player = actors.Player([50,50], self.player_singleton, 
                                        self.all_sprites)        

    def make_walls(self):
        x = 0
        y = 0
        walls = pg.sprite.LayeredDirty()
        for row in WORLD:
            for col in row:
                if col == "#":
                    Wall((x,y), walls, self.all_sprites)
                x += WALL_SIZE
            y += WALL_SIZE
            x = 0

        return walls

    def make_enemies(self):
        enemies = pg.sprite.LayeredDirty()
        while len(enemies) < self.max_enemies:
            x = random.randint(0, util.SCREEN_WIDTH)
            y = random.randint(0, util.SCREEN_HEIGHT)
            bug = actors.Bug((x, y))
            if not pg.sprite.spritecollideany(bug, self.walls):
                bug.add(enemies, self.all_sprites)

        return enemies

    def handle_events(self, event):
        self.player.handle_events(event)

    def update(self, dt, current_time, keys):       
        self.player_singleton.update(dt, keys, self.enemies, self.walls)
        self.enemies.update(dt, current_time, self.walls)
        util.gfx_group.update(dt)

        for sprite in self.all_sprites:
            layer = self.all_sprites.get_layer_of_sprite(sprite)
            if layer != sprite.rect.bottom:
                self.all_sprites.change_layer(sprite, sprite.rect.bottom)

        hits = pg.sprite.groupcollide(self.walls, util.gfx_group, False, True)
        if hits:
            for wall in hits:
                wall.dirty = 1

    def render(self, surface):
        rects1 = util.gfx_group.draw(surface)
        rects2 = self.all_sprites.draw(surface)
        return rects1 + rects2


class Wall(pg.sprite.DirtySprite):
    """docstring for Wall"""
    def __init__(self, pos, *gorups):
        super(Wall, self).__init__(*gorups)
        self.image = pg.Surface((WALL_SIZE, WALL_SIZE))
        self.image.fill((155,255,155))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.dirty = 1
        