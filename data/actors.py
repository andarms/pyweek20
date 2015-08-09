import pygame as pg

import util

class Player(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super(Player, self).__init__(*groups)
        self.pos = pos
        self.image = pg.Surface((20,50))
        self.image.fill((56,185,174))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 100 #px/seg
        self.direction = None

    def update(self, dt, keys):
        for key in util.CONTROLS:
            if keys[key]:
                self.direction = util.CONTROLS[key]
                direction_vector = util.DIR_VECTORS[self.direction]
                self.pos[0] += direction_vector[0] * self.speed * dt
                self.pos[1] += direction_vector[1] * self.speed * dt

                self.rect.topleft = self.pos