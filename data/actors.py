import math
import random
import itertools

import pygame as pg

import util, hud

def hit_rect_collide(left, right):
    return left.hit_rect.colliderect(right.rect)

class Actor(pg.sprite.Sprite):
    """docstring for Actor"""
    def __init__(self, pos, spritesheet, size, *groups):
        super(Actor, self).__init__(*groups)
        self.speed = 250 #px/seg
        self.direction = "DOWN"
        self.old_direction = None
        self.direction_stack = []
        self.cooldowntime = 0.1 #seg
        self.cooldown = 0.5
        self.is_explosive = False
        self.hp = 100
        self.collide = False
        self.animate_timer  = 0.0
        self.animate_fps = 10.0
        self.size = size
        self.idelframes = {}
        self.walkframes = None
        self.frames = self.make_frame_dict(self.get_frames(spritesheet))
        self.dirty = 1
        self.animate()
        self.rect = self.image.get_rect(topleft=pos)
        self.hit_rect = self.rect.copy()
        self.hit_rect.midbottom = self.rect.midbottom  

    def get_frames(self, spritesheet):
        """ Must be overloaded in child objects"""
        pass

    def make_frame_dict(self, frames):
        """ Must be overloaded in child objects"""
        pass

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

    def update(self, dt, now, walls):
        self.animate(now)
        if self.hp <= 0:
            self.kill()
        if self.direction_stack:
            direction_vector = util.DIR_VECTORS[self.direction]
            self.rect.x += direction_vector[0] * self.speed * dt
            self.rect.y += direction_vector[1] * self.speed * dt
            self.hit_rect.center = self.rect.center
        self.check_collitions(walls)    

    def animate(self, now=0):
        if self.direction != self.old_direction:
            self.walkframes = self.frames[self.direction]
            self.old_direction = self.direction
            self.dirty = 1
        if self.dirty or now-self.animate_timer > 1000/self.animate_fps:
            if self.direction_stack:
                self.image = next(self.walkframes)
                self.animate_timer = now
                self.dirty = 0
            else:
                self.image = self.idelframes[self.direction]


    def check_collitions(self, walls):
        wall = pg.sprite.spritecollideany(self, walls, hit_rect_collide)
        if wall:
            if self.direction == "LEFT":
                self.hit_rect.left = wall.rect.right
            elif self.direction == "RIGHT":
                self.hit_rect.right = wall.rect.left
            elif self.direction == "UP":
                self.hit_rect.top = wall.rect.bottom                    
            elif self.direction == "DOWN":
                self.hit_rect.bottom = wall.rect.top
            self.rect.center = self.hit_rect.center
            self.collide = True
        else:
            self.collide = False

    def attack(self, dt, direction=None, *groups):
        if not direction:
            direction = self.direction
        if self.cooldown > 0:
            self.cooldown -= dt
        else:
            Bullet(self.rect.center, direction, self.bullet_color,  *groups)
            self.cooldown = self.cooldowntime

    def take_damage(self, damage):
        self.hp -= damage
        self.dirty = 1
        if self.hp <= 0:
            return self.value

    def kill(self, exploded=False):
        super(Actor, self).kill()
        for _ in xrange(random.randint(25,50)):
            Fragment(self.rect.center)
        if not exploded:
            hud.KillLabel(self.rect.topleft, self.value)
        del self

class Player(Actor):
    def __init__(self, pos, *groups):
        size = (32,64)
        image = "player"
        super(Player, self).__init__(pos, image, size, *groups)
        self.speed = 300
        self.bullets = pg.sprite.Group()
        self.cooldowntime = 0.4
        self.score = 0
        self.value = 0
        self.hit_rect.h = self.rect.h-22
        self.bullet_color = (51, 255, 255)

    def make_frame_dict(self, frames):
        frame_dict = {}
        for i,direct in enumerate(util.DIRECTIONS):
            self.idelframes[direct] = frames[i][0]
            frame_dict[direct] = itertools.cycle(frames[i])
        return frame_dict

    def get_frames(self, spritesheet):
        sheet = util.GFX[spritesheet]
        all_frames = util.split_sheet(sheet, self.size, 4, 4)
        return all_frames

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

    def update(self, dt, now, keys, enemies, walls):
        super(Player, self).update(dt, now, walls)
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
            damage = random.randint(5,40)
            value = bug.take_damage(damage)
            if value:
                self.score += value

class Bug(Actor):
    """docstring for Bug"""
    def __init__(self, pos, image=None, *groups):
        size = (32,32)
        if not image: image = "bug"
        super(Bug, self).__init__(pos, image, size, *groups)
        self.wait_range = (500, 2000)
        self.wait_delay = random.randint(*self.wait_range)
        self.wait_time = 0.0
        self.change_direction()
        self.value = 10
        self.is_explosive = True
        self.animate_fps = 5.0

    def make_frame_dict(self, frames):
        frame_dict = {}
        for i,direct in enumerate(util.DIRECTIONS):
            self.idelframes[direct] = frames[i][0]
            frame_dict[direct] = itertools.cycle(frames[i])
        return frame_dict

    def get_frames(self, spritesheet):
        sheet = util.GFX[spritesheet]
        all_frames = util.split_sheet(sheet, self.size, 3, 4)
        return all_frames

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            self.add_direction(event.key)                       
        if event.type == pg.KEYUP:
            self.pop_direction(event.key)

    def update(self, dt, now, walls, *args):
        """
        Choose a new direction if wait_time has expired or the sprite
        collide with thw walls.
        """        
        if now-self.wait_time > self.wait_delay:
            self.change_direction(now)
        super(Bug, self).update(dt, now, walls)
        if self.collide:
            self.change_direction(now)


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
    def __init__(self, pos, image, *groups):
        super(ChasingBug, self).__init__(pos, "kamikaze", *groups)
        self.wait_delay = 500 #mseg
        self.value = 15

    def update(self, dt, now, walls, player):
        """
        Simple chasing, random choose to follow the player
        vertical or horizontal.
        Player rect player.rect pg.Rect
        """
        if now-self.wait_time > self.wait_delay:
            x_diff = self.rect.x - player.rect.x
            y_diff = self.rect.y - player.rect.y
            first = random.choice(('vertical', 'horizontal'))
            if first == 'horizontal':
                if x_diff < 0: direction = "RIGHT"
                else: direction = "LEFT"
            else:
                if y_diff < 0: direction = "DOWN"
                else: direction = "UP"
            self.change_direction(now, direction)
        super(Bug, self).update(dt, now, walls)
        if self.collide:
            self.change_direction(now)

class ErrorBlock(Bug):
    """docstring for ErrorBlock"""
    def __init__(self, pos, *groups):
        super(ErrorBlock, self).__init__(pos, "Error", *groups)

class Virus(Bug):
    """docstring for Virus"""
    def __init__(self, pos, image,*groups):
        super(Virus, self).__init__(pos, "virus", *groups)
        self.hp = 300
        self.is_explosive = None
        self.bullets = pg.sprite.Group()
        self.bullet_color = (51, 51, 255)
        self.cooldowntime = 0.5

    def make_frame_dict(self, frames):
        frame_dict = {}
        for direct in util.DIRECTIONS:
            self.idelframes[direct] = frames[0][0]
            frame_dict[direct] = itertools.cycle(frames[0])
        return frame_dict

    def update(self, dt, now, walls, player):
        """
        Simple chasing, random choose to follow the player
        vertical or horizontal.
        Player rect player.rect pg.Rect
        """
        if now-self.wait_time > self.wait_delay:
            x_diff = self.rect.x - player.rect.x
            y_diff = self.rect.y - player.rect.y
            first = random.choice(('vertical', 'horizontal'))
            if first == 'horizontal':
                if x_diff < 0: direction = "LEFT"
                else: direction = "RIGHT"
            else:
                if y_diff < 0: direction = "UP"
                else: direction = "DOWN"
            self.change_direction(now, direction)

        x_sight = self.rect.x in xrange(player.rect.x-32, player.rect.x+32)
        y_sight = self.rect.y in xrange(player.rect.y-32, player.rect.y+32)
        if y_sight and self.direction in ("LEFT", "RIGHT"): 
            self.attack(dt, self.direction, self.bullets)
        if x_sight and self.direction in ("UP", "DOWN"):
            self.attack(dt, self.direction, self.bullets)
        if pg.sprite.spritecollide(player, self.bullets,True):
            damage = random.randint(5,15)
            player.take_damage(damage)
            hud.DamageLabel(player.rect.topleft, damage)

        super(Bug, self).update(dt, now, walls)
        if self.collide:
            self.change_direction(now)



    def get_frames(self, spritesheet):
        sheet = util.GFX[spritesheet]
        all_frames = util.split_sheet(sheet, self.size, 2, 1)
        return all_frames
        
        
        
class Trojan(Actor):
    def __init__(self, pos, *groups):
        size = (32,64)
        image = "trojan"
        super(Trojan, self).__init__(pos, image, size, *groups)
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
        self.bullet_color = (100, 100, 100)

    def make_frame_dict(self, frames):
        frame_dict = {}
        for i,direct in enumerate(util.reverse_dirs):
            self.idelframes[direct] = frames[i][0]
            frame_dict[direct] = itertools.cycle(frames[i])
        return frame_dict

    def get_frames(self, spritesheet):
        sheet = util.GFX[spritesheet]
        all_frames = util.split_sheet(sheet, self.size, 4, 4)
        return all_frames

    def update(self, dt, now, walls, player):
        """
        Better Chase. Still not been the better AI but work for me.
        """
        if now-self.wait_time > self.wait_delay:
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
            self.wait_time = now
        
        # Attack if player
        x_sight = self.rect.x in xrange(player.rect.x-32, player.rect.x+32)
        y_sight = self.rect.y in xrange(player.rect.y-32, player.rect.y+32)
        if y_sight and self.direction in ("LEFT", "RIGHT"): 
            self.attack(dt, self.direction, self.bullets)
        if x_sight and self.direction in ("UP", "DOWN"):
            self.attack(dt, self.direction, self.bullets)
        if pg.sprite.spritecollide(player, self.bullets,True):
            damage = random.randint(5,15)
            player.take_damage(damage)
            hud.DamageLabel(player.rect.topleft, damage)

        # movement
        if self.reach_goal():
            self.pop_direction(self.direction)
            if self.next_direction:
                self.add_direction(self.next_direction)
                self.next_direction = None
        super(Trojan, self).update(dt, now, walls)          
        if self.collide:            
            self.pop_direction(self.direction)
            new_direction = random.choice(util.DIRECTIONS)            
            self.add_direction(new_direction)
            self.wait_time = now

    def reach_goal(self):
        if self.rect.x == self.goal_x or self.rect.y == self.goal_y:            
            return True
        return False


class Fragment(pg.sprite.Sprite):
    """Explosions fragments"""
    def __init__(self, pos, layer = 9, *groups):
        super(Fragment, self).__init__(*groups)
        self.add(util.gfx_group)

        self.pos = [0.0,0.0]
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self._layer = layer
        self.max_speed = 50
        self.dx = random.randint(-self.max_speed, self.max_speed)
        self.dy = random.randint(-self.max_speed, self.max_speed)
        self.lifetime = 1.5
        self.image = pg.Surface((10,10))
        self.image.set_colorkey((0,0,0))
        color = random.randint(25,255)
        self.color = (color, color, color)
        size = random.randint(2,5)
        pg.draw.rect(self.image, self.color, (0,0, size, size))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.time = 0.0
        
    def update(self, seconds):
        self.time += seconds
        if self.time > self.lifetime:
            self.kill() 
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds
        self.rect.centerx = round(self.pos[0],0)
        self.rect.centery = round(self.pos[1],0)
    

class Bullet(pg.sprite.Sprite):
    """docstring for Bullet"""
    def __init__(self, pos, direction, color, *groups):
        super(Bullet, self).__init__(*groups)
        self.add(util.gfx_group, util.bullets_group)
        self.lifetime = 3 #seg
        self.color = color
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