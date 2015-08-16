import random
import pygame as pg

from pytmx.util_pygame import load_pygame
from ... import util, actors, hud

class Level(object):
    """docstring for Level"""
    def __init__(self, player):
        self.max_enemies = 18
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.map_sprites = pg.sprite.Group()
        self.actions = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.visible_sprites = pg.sprite.LayeredUpdates()
        self.player_singleton = pg.sprite.GroupSingle()

        self.world_map = load_pygame(util.MAPS.pop())
        w = self.world_map.width*util.WALL_SIZE
        h = self.world_map.height*util.WALL_SIZE
        self.image = pg.Surface((w,h))
        self.rect = self.image.get_rect()        
        player.add(self.player_singleton, self.all_sprites)
        self.enemies = self.make_enemies()
        self.make_level()
        self.viewport = Viewport()
        self.viewport.update(self.player_singleton.sprite, self.rect)


    def make_level(self):
        layer = self.world_map.layers[0]
        collision = self.world_map.layers[1]
        infecteds = self.world_map.layers[2]
        for x, y, image in layer.tiles():
                tile = pg.sprite.Sprite(self.map_sprites, self.all_sprites)
                tile.image = image
                tile.rect = pg.Rect(x*64, y*64, 64,64)
                if random.random() > .66:
                    self.player_singleton.sprite.rect.topleft = x*64, y*64
        for x, y, image in collision.tiles():
            Wall((x*64,y*64), image, self.walls, self.all_sprites)
        for x, y, image in  infecteds.tiles():
            normal_image = self.world_map.get_tile_image(x, y, 1)
            iwall = InfectedWall((x*64,y*64), image, normal_image, self.actions)
            iwall.add(self.all_sprites, self.walls)
        
        



    def make_enemies(self):
        enemies = pg.sprite.Group()
        bugs = int (self.world_map.properties["bugs"])
        chasing = int (self.world_map.properties["chasing"])
        for _ in xrange(bugs):
            x = random.randint(0, self.rect.w)
            y = random.randint(0, self.rect.h)
            bug = actors.Bug((x, y), None)
            if not pg.sprite.spritecollideany(bug, self.walls):
                bug.add(enemies, self.all_sprites)
        for _ in xrange(chasing):
            x = random.randint(0, self.rect.w)
            y = random.randint(0, self.rect.h)
            bug = actors.ChasingBug((x, y), None)
            if not pg.sprite.spritecollideany(bug, self.walls):
                bug.add(enemies, self.all_sprites)
        return enemies

    def update(self, dt, now, keys):
        self.player_singleton.update(dt, now, keys, self.enemies, self.walls)
        player = self.player_singleton.sprite
        self.enemies.update(dt, now, self.walls, player)
        self.actions.update(dt, now, player, keys)
        util.gfx_group.update(dt)
        self.viewport.update(self.player_singleton.sprite, self.rect)
        

        visible_sprites = pg.sprite.spritecollide(self.viewport, self.all_sprites, False)
        self.visible_sprites.add(visible_sprites)
        for sprite in self.visible_sprites.sprites():
            if not sprite in self.map_sprites:
                self.visible_sprites.change_layer(sprite, sprite.rect.bottom)                
            if sprite not in visible_sprites:
                self.visible_sprites.remove(sprite)

        # Remove bullets when collides with walls
        pg.sprite.groupcollide(self.walls, util.bullets_group, False, True)    

    def is_clear(self):
        if not self.actions:
            return True
        return False

    def render(self, surface):
        self.image.fill((0,0,0))
        self.visible_sprites.draw(self.image)
        util.gfx_group.draw(self.image)
        surface.blit(self.image, (0,0), self.viewport)       

class Viewport(object):
    """docstring for viewport"""
    def __init__(self):
        self.rect = util.SCREEN_RECT.copy()

    def update(self, player, screen_rect):
        self.rect.center = player.rect.center
        self.rect.clamp_ip(screen_rect)
        

class Wall(pg.sprite.Sprite):
    """docstring for Wall"""
    def __init__(self, pos, image, *gorups):
        super(Wall, self).__init__(*gorups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self._layer = self.rect.bottom
        self.dirty = 1

class InfectedWall(pg.sprite.Sprite):
    """docstring for Wall"""
    def __init__(self, pos, image, normal_image, action, *gorups):
        super(InfectedWall, self).__init__(*gorups)
        self.image = image
        self.normal_image = normal_image
        # group to manage the aumont of infected walls
        self.action = action 
        self.add(self.action)
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.h += 1 # to draw order
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
        self.infected = True

    def kill(self):
        self.tooltip.kill()
        self.image = self.normal_image
        self.infected = False
        self.remove(self.action)      
        return False

    def update(self, dt, now, player, keys):
        if self.infected:
            if self.death == 100:
                player.dirty = 1
                player.score += random.randint(20,50)
                hud.SuccessLabel(self.big_rect.topleft, "Deleted")
                return self.kill()
            else:
                if self.big_rect.colliderect(player.rect):
                    self.tooltip.add(util.gfx_group)
                    if keys[pg.K_e]:
                        self.deleting = True
                else:
                    self.tooltip.remove(util.gfx_group)
                    self.deleting = False
                    self.death = 0      
                    self.tooltip.change_text(self.help_text)
                if now-self.time > self.delay:
                    if self.deleting:
                        self.tooltip.change_text("Deleting %d" % (self.death))
                        self.death += 1
                    self.time = now