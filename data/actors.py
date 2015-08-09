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

    def update(self, dt):
        if self.direction_stack:
            direction_vector = util.DIR_VECTORS[self.direction]
            self.rect.x += direction_vector[0] * self.speed * dt
            self.rect.y += direction_vector[1] * self.speed * dt

        self.rect.clamp_ip(util.SCREEN_RECT)