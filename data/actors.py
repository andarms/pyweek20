import pygame as pg

import util

class Player(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super(Player, self).__init__(*groups)
        self.pos = pos
        self.image = pg.Surface((32,32))
        self.image.fill((56,185,174))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 200 #px/seg
        self.direction = "UP"
        self.direction_stack = []
        self.cooldowntime = 0.3 #seg
        self.cooldown = 0.0

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            self.add_direction(event.key)                       
        if event.type == pg.KEYUP: 
            self.pop_direction(event.key)

    def add_direction(self, key):
        """
        Add direction to the sprite's direction stack and change current
        direction.
        """
        if key in util.CONTROLS:
            direction = util.CONTROLS[key]
            if direction in self.direction_stack:
                self.direction_stack.remove(direction)
            self.direction_stack.append(direction)
            self.direction = direction

    def pop_direction(self, key):
        """
        Remove direction from direction stack and change current direction
        to the top of the stack (if not empty).
        """
        if key in util.CONTROLS:
            direction = util.CONTROLS[key]
            if direction in self.direction_stack:
                self.direction_stack.remove(direction)
            if self.direction_stack:
                self.direction = self.direction_stack[-1]

    def update(self, dt, keys):
        if self.direction_stack:
            direction_vector = util.DIR_VECTORS[self.direction]
            self.rect.x += direction_vector[0] * self.speed * dt
            self.rect.y += direction_vector[1] * self.speed * dt

        if self.cooldown > 0:
            self.cooldown -= dt
        else:
            if keys[pg.K_d]:
                Bullet(self.rect.center, self.direction)
                self.cooldown = self.cooldowntime



        self.rect.clamp_ip(util.SCREEN_RECT)


class Bullet(pg.sprite.Sprite):
    """docstring for Bullet"""
    def __init__(self, pos, direction):
        super(Bullet, self).__init__()
        self.add(util.gfx_group)
        self.lifetime = 3 #seg
        self.color = (255, 51, 51)
        self.image = pg.Surface((10, 10))
        # self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        # pg.draw.circle(self.image, self.color, self.rect.center, 5)
        # self.image = self.image.convert_alpha()
        self.direction = util.DIR_VECTORS[direction]
        self.time = 0.0
        self.speed = 350
        self.dx = self.direction[0] * self.speed
        self.dy = self.direction[1] * self.speed        

    def update(self, dt):
        self.time += dt
        if self.time > self.lifetime:
            self.kill() 
        self.rect.centerx += self.dx * dt
        self.rect.centery += self.dy * dt