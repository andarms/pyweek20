import math
import random

import pygame as pg

import util
class Actor(pg.sprite.Sprite):
    """docstring for Actor"""
    def __init__(self, pos, *groups):
        super(Actor, self).__init__(*groups)
        self.pos = pos
        self.image = pg.Surface((32,32)) # replace for image load
        self.image.fill((56,185,174))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 250 #px/seg
        self.direction = "UP"
        self.direction_stack = []
        self.cooldowntime = 0.1 #seg
        self.cooldown = 0.0
        self.hp = 100

    def add_direction(self, direction):
        """
        Add direction to the sprite's direction stack and change current
        direction.
        """
        if direction in self.direction_stack:
            self.direction_stack.remove(direction)
        self.direction_stack.append(direction)
        self.direction = direction

    def pop_direction(self, direction):
        """
        Remove direction from direction stack and change current direction
        to the top of the stack (if not empty).
        """
        if direction in self.direction_stack:
            self.direction_stack.remove(direction)
        if self.direction_stack:
            self.direction = self.direction_stack[-1]

    def update(self, dt):
        if self.hp <= 0:
            self.kill()
        if self.direction_stack:
            direction_vector = util.DIR_VECTORS[self.direction]
            self.rect.x += direction_vector[0] * self.speed * dt
            self.rect.y += direction_vector[1] * self.speed * dt
        self.rect.clamp_ip(util.SCREEN_RECT)

    def attack(self, dt, *groups):
        if self.cooldown > 0:
            self.cooldown -= dt
        else:
            Bullet(self.rect.center, self.direction, *groups)
            self.cooldown = self.cooldowntime

class Player(Actor):
    def __init__(self, pos, *groups):
        super(Player, self).__init__(pos, *groups)
        self.image.fill((56,153,253))
        self.speed = 300
        self.bullets = pg.sprite.Group()

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            self.add_direction(event.key)                       
        if event.type == pg.KEYUP: 
            self.pop_direction(event.key)

    def add_direction(self, key):
        if key in util.CONTROLS:
            direction = util.CONTROLS[key]
            super(Player, self).add_direction(direction)

    def pop_direction(self, key):
        if key in util.CONTROLS:
            direction = util.CONTROLS[key]
            super(Player, self).pop_direction(direction)

    def update(self, dt, keys, enemies):
        super(Player, self).update(dt)
        if keys[pg.K_d]:
            self.attack(dt, self.bullets)
        hits = pg.sprite.groupcollide(enemies, self.bullets, False, True)
        for bug in hits:
            bug.hp -= 35 # just one hit for bullet allow

class Bug(Actor):
    """docstring for Bug"""
    def __init__(self, pos, *groups):
        super(Bug, self).__init__(pos, *groups)
        self.wait_range = (500, 3000)
        self.wait_delay = random.randint(*self.wait_range)
        self.wait_time = 0.0
        self.change_direction()

    def update(self, dt, current_time):
        """
        Choose a new direction if wait_time has expired or the sprite
        attempts to leave the screen.
        """        
        if current_time-self.wait_time > self.wait_delay:
            self.change_direction(current_time)
        super(Bug, self).update(dt)
        if not util.SCREEN_RECT.contains(self.rect):
            self.change_direction(current_time)
            self.rect.clamp_ip(util.SCREEN_RECT)

    def change_direction(self, now=0):
        """
        Empty the stack and choose a new direction.  The sprite may also
        choose not to go idle (choosing direction=None)
        """
        self.direction_stack = []
        direction = random.choice(util.DIRECTIONS+(None,))
        if direction:
            super(Bug, self).add_direction(direction)
        self.wait_delay = random.randint(*self.wait_range)
        self.wait_time = now

    def distance(self, p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[0])**2)

        

class Bullet(pg.sprite.Sprite):
    """docstring for Bullet"""
    def __init__(self, pos, direction, *groups):
        super(Bullet, self).__init__(*groups)
        self.add(util.gfx_group)
        self.lifetime = 3 #seg
        self.color = (255, 51, 51)
        w, h= (10, 2)
        if direction == "UP" or direction == "DOWN":
            w, h = h, w
        self.image = pg.Surface((w,h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=pos)
        self.direction = util.DIR_VECTORS[direction]
        self.time = 0.0
        self.speed = 450
        self.dx = self.direction[0] * self.speed
        self.dy = self.direction[1] * self.speed        

    def update(self, dt):
        self.time += dt
        if self.time > self.lifetime:
            self.kill() 
        self.rect.centerx += self.dx * dt
        self.rect.centery += self.dy * dt