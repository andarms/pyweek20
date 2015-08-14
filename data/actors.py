import math
import random

import pygame as pg

import util, hud

class Actor(pg.sprite.Sprite):
    """docstring for Actor"""
    def __init__(self, pos, *groups):
        super(Actor, self).__init__(*groups)
        self.pos = pos
        self.image = pg.Surface((32,32)) # replace for image load
        self.image.fill((226,51,74))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 250 #px/seg
        self.direction = "UP"
        self.direction_stack = []
        self.cooldowntime = 0.1 #seg
        self.cooldown = 0.0
        self.is_explosive = False
        self.hp = 100
        self.collide = False
        self.dirty = 1

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

    def update(self, dt, walls):
        if self.hp <= 0:
            self.kill()
        if self.direction_stack:
            self.dirty = 1
            direction_vector = util.DIR_VECTORS[self.direction]
            self.rect.x += direction_vector[0] * self.speed * dt
            self.rect.y += direction_vector[1] * self.speed * dt
        self.check_collitions(walls)

    def check_collitions(self, walls):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.direction == "LEFT":
                    self.rect.left = wall.rect.right
                elif self.direction == "RIGHT":
                    self.rect.right = wall.rect.left
                elif self.direction == "UP":
                    self.rect.top = wall.rect.bottom                    
                elif self.direction == "DOWN":
                    self.rect.bottom = wall.rect.top
                self.collide = True
                self.dirty = 1
            else:
                self.collide = False

    def attack(self, dt, direction=None, *groups):
        self.dirty = 1
        if not direction:
            direction = self.direction
        if self.cooldown > 0:
            self.cooldown -= dt
        else:
            Bullet(self.rect.center, direction, *groups)
            self.cooldown = self.cooldowntime

    def take_damage(self, damage):
        self.hp -= damage
        self.dirty = 1
        if self.hp <= 0:
            return self.value

    def kill(self, exploded=False):
        super(Actor, self).kill()
        if not exploded:
            hud.KillLabel(self.rect.topleft, self.value)
        del self

class Player(Actor):
    def __init__(self, pos, *groups):
        super(Player, self).__init__(pos, *groups)
        self.image.fill((56,153,253))
        self.speed = 300
        self.bullets = pg.sprite.Group()
        self.cooldowntime = 0.4
        self.score = 0
        self.value = 0

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

    def update(self, dt, keys, enemies, walls):
        super(Player, self).update(dt, walls)
        # Shooting
        for key in util.ATTACK_KEYS:
            if keys[key]:
                self.attack(dt, util.ATTACK_KEYS[key], self.bullets)
        # Collisions with enemies
        enes = pg.sprite.spritecollide(self, enemies, False)
        if enes:
            for e in enes:
                if e.is_explosive:
                    damage = random.randint(5,10)
                    self.take_damage(damage)
                    hud.DamageLabel(self.rect.topleft, damage)
                    e.kill(True)
        # Bullests collisions with enemies
        hits = pg.sprite.groupcollide(enemies, self.bullets, False, True)
        for bug in hits:
            value = bug.take_damage(35)
            if value:
                self.score += value

class Bug(Actor):
    """docstring for Bug"""
    def __init__(self, pos, *groups):
        super(Bug, self).__init__(pos, *groups)
        self.wait_range = (500, 2000)
        self.wait_delay = random.randint(*self.wait_range)
        self.wait_time = 0.0
        self.change_direction()
        self.value = 10
        self.is_explosive = True

    def update(self, dt, current_time, walls, *args):
        """
        Choose a new direction if wait_time has expired or the sprite
        collide with thw walls.
        """        
        if current_time-self.wait_time > self.wait_delay:
            self.change_direction(current_time)
        super(Bug, self).update(dt, walls)
        if self.collide:
            self.change_direction(current_time)


    def change_direction(self, now=0, direction=None):
        """
        Empty the stack and choose a new direction.  The sprite may also
        choose not to go idle (choosing direction=None)
        """
        self.direction_stack = []
        if not direction:
            direction = random.choice(util.DIRECTIONS+(None,))
        if direction:
            super(Bug, self).add_direction(direction)
        self.wait_delay = random.randint(*self.wait_range)
        self.wait_time = now

    def distance(self, p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[0])**2)


class ChasingBug(Bug):
    def __init__(self, pos, *groups):
        super(ChasingBug, self).__init__(pos, *groups)
        self.image.fill((182,185,52))
        self.wait_delay = 500 #mseg
        self.value = 15

    def update(self, dt, current_time, walls, player):
        """
        Simple chasing, random choose to follow the player
        vertical or horizontal.
        Player rect player.rect pygame.Rect
        """
        if current_time-self.wait_time > self.wait_delay:
            x_diff = self.rect.x - player.rect.x
            y_diff = self.rect.y - player.rect.y
            first = random.choice(('vertical', 'horizontal'))
            if first == 'horizontal':
                if x_diff < 0: direction = "RIGHT"
                else: direction = "LEFT"
            else:
                if y_diff < 0: direction = "DOWN"
                else: direction = "UP"
            self.change_direction(current_time, direction)
        super(Bug, self).update(dt, walls)
        if self.collide:
            self.change_direction(current_time)
        
class Trojan(Actor):
    def __init__(self, pos, *groups):
        super(Trojan, self).__init__(pos, *groups)
        self.image.fill((200,200,200))
        self.wait_range = (500, 800)
        self.wait_delay = random.randint(*self.wait_range)
        self.wait_time = 0.0
        self.goal_x = 0
        self.goal_y = 0        
        self.next_direction = None
        self.hp = 250
        self.cooldowntime = 0.5
        self.bullets = pg.sprite.Group()
        self.value = 50

    def update(self, dt, current_time, walls, player):
        """
        Better Chase. Still not been the better AI but work for me.
        """
        if current_time-self.wait_time > self.wait_delay:
            self.direction_stack = []
            self.goal_x = player.rect.x
            self.goal_y = player.rect.y
            x_diff = self.rect.x - player.rect.x
            y_diff = self.rect.y - player.rect.y
            if not x_diff in xrange(-32,32) or not y_diff in xrange(-32,32):
                if x_diff < 0: dir_x = "RIGHT"
                else: dir_x = "LEFT"
                if y_diff < 0: dir_y = "DOWN"
                else: dir_y = "UP"
                first = random.choice(('vertical', 'horizontal'))
                if first == 'horizontal':
                    self.add_direction(dir_x)
                    self.next_direction = dir_y
                else:
                    self.add_direction(dir_y)
                    self.next_direction = dir_x
            self.wait_time = current_time
        
        # Attack if player
        x_sight = self.rect.x in xrange(player.rect.x-32, player.rect.x+32)
        y_sight = self.rect.y in xrange(player.rect.y-32, player.rect.y+32)
        if y_sight and self.direction in ("LEFT", "RIGHT"): 
            self.attack(dt, self.direction, self.bullets)
        if x_sight and self.direction in ("UP", "DOWN"):
            self.attack(dt, self.direction, self.bullets)
        if pg.sprite.spritecollide(player, self.bullets,True):
            player.take_damage(5)

        # movement
        if self.reach_goal():
            self.pop_direction(self.direction)
            if self.next_direction:
                self.add_direction(self.next_direction)
                self.next_direction = None
        super(Trojan, self).update(dt, walls)          
        if self.collide:            
            self.pop_direction(self.direction)
            new_direction = random.choice(util.DIRECTIONS)            
            self.add_direction()
            self.wait_time = current_time

    def reach_goal(self):
        if self.rect.x == self.goal_x or self.rect.y == self.goal_y:            
            return True
        return False



class Bullet(pg.sprite.Sprite):
    """docstring for Bullet"""
    def __init__(self, pos, direction, *groups):
        super(Bullet, self).__init__(*groups)
        self.add(util.gfx_group, util.bullets_group)
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
        self.dirty = 2  

    def update(self, dt):
        self.time += dt
        if self.time > self.lifetime:
            self.kill() 
        self.rect.centerx += self.dx * dt
        self.rect.centery += self.dy * dt