import random
import pygame as pg

from ... import util, actors, hud

def clear_callback(surface, rect):
    """
    We need this callback because the clearing background contains
    transparency.  We need to fill the rect with transparency first.
    """
    surface.fill((0,0,0,0), rect)

class Level(object):
    """docstring for Level"""
    def __init__(self):
        w = len(util.WORLD[0])*util.WALL_SIZE
        h = len(util.WORLD)*util.WALL_SIZE
        self.image = pg.Surface((w,h))
        self.rect = self.image.get_rect()
        self.background = pg.Surface(self.image.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        self.max_enemies = 27
        self.all_sprites = pg.sprite.LayeredDirty()
        self.actions = pg.sprite.Group()
        self.walls = self.make_walls()
        self.enemies = self.make_enemies()
        self.player_singleton = pg.sprite.GroupSingle()
        self.player = actors.Player([50,50], self.player_singleton, 
                                        self.all_sprites)
        self.viewport = util.SCREEN_RECT.copy()
        self.hud = hud.HUD()

    def make_walls(self):
        x = 0
        y = 0
        walls = pg.sprite.LayeredDirty()
        for row in util.WORLD:
            for col in row:
                if col == "#":
                    Wall((x,y), walls, self.all_sprites)
                if col == "=":
                    InfectedWall((x,y), walls, self.actions, self.all_sprites)
                x += util.WALL_SIZE
            y += util.WALL_SIZE
            x = 0

        return walls

    def make_enemies(self):
        enemies = pg.sprite.LayeredDirty()
        while len(enemies) < self.max_enemies:
            x = random.randint(0, self.rect.w)
            y = random.randint(0, self.rect.h)
            bug = actors.Bug((x, y))
            if not pg.sprite.spritecollideany(bug, self.walls):
                bug.add(enemies, self.all_sprites)
        x = random.randint(0, self.rect.w)
        y = random.randint(0, self.rect.h)
        actors.Trojan((x, y), enemies, self.all_sprites)
        return enemies

    def handle_events(self, event):
        self.player.handle_events(event)

    def update(self, dt, current_time, keys):       
        self.player_singleton.update(dt, keys, self.enemies, self.walls)
        self.enemies.update(dt,current_time, self.walls, self.player)
        self.actions.update(dt, current_time, self.player, keys)
        util.gfx_group.update(dt)
        self.update_viewport()
        self.hud.update(self.player)

        for sprite in self.all_sprites:
            layer = self.all_sprites.get_layer_of_sprite(sprite)
            if layer != sprite.rect.bottom:
                self.all_sprites.change_layer(sprite, sprite.rect.bottom)

        hits = pg.sprite.groupcollide(self.walls, util.gfx_group, False, True)
        if hits:
            for wall in hits:
                wall.dirty = 1

    def update_viewport(self):
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.rect)

    def render(self, surface):
        dirty = []
        util.gfx_group.clear(self.image, self.background)
        self.all_sprites.clear(self.image, self.background)
        self.all_sprites.draw(self.image)
        util.gfx_group.draw(self.image)
        rect1 = surface.blit(self.image, (0,0), self.viewport)
        rect2 = self.hud.render(surface)
        dirty.extend((rect1, rect2))
        return dirty



class Wall(pg.sprite.DirtySprite):
    """docstring for Wall"""
    def __init__(self, pos, *gorups):
        super(Wall, self).__init__(*gorups)
        self.image = pg.Surface((util.WALL_SIZE, util.WALL_SIZE))
        self.image.fill((155,255,155))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.dirty = 1

class InfectedWall(pg.sprite.DirtySprite):
    """docstring for Wall"""
    def __init__(self, pos, *gorups):
        super(InfectedWall, self).__init__(*gorups)
        self.image = pg.Surface((util.WALL_SIZE, util.WALL_SIZE))
        self.image.fill((55,100,25))
        self.rect = self.image.get_rect(topleft=pos)
        self.big_rect = self.rect.copy()
        self.big_rect.inflate_ip(15,10)
        self.big_rect.center = self.rect.center
        self.help_text = "Prees E to Delete it"
        self.tooltip = hud.Tooltip(self.help_text, self.rect.center)
        self.deleting = False
        self.death = 0
        self.dirty = 1
        self.time = 0.0
        self.delay = 50
        

    def update(self, dt, current_time, player, keys):
        if self.death == 100:
            self.kill()
            self.tooltip.kill()
            del self
            return False

        if self.big_rect.colliderect(player.rect):
            self.tooltip.add(util.gfx_group)
            if keys[pg.K_e]:
                self.deleting = True
        else:
            self.tooltip.remove(util.gfx_group)
            self.deleting = False
            self.death = 0      
            self.tooltip.change_text(self.help_text)
        if current_time-self.time > self.delay:
            if self.deleting:
                self.tooltip.change_text("Deleting %d" % (self.death))
                self.death += 1
            self.time = current_time



