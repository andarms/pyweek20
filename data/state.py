import pygame as pg

import util

class StateManager(object):
    """ Control class for the games states"""
    def __init__(self):
        self.bg_color = (0,0,0)
        self.caption = util.CAPTION        
        self.screen = pg.display.get_surface()
        self.screen_size = util.SCREEN_SIZE
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.show_fps = True
        self.done = False
        self.keys = pg.key.get_pressed()        
        self.state_dict = {}
        self.state = None
        self.state_name = None

    def setup_states(self, state_dict, start_state):
        """ state_dict in a dict with a instance of each state of the game"""
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)

            if event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

            self.state.handle_events(event)

    def toggle_show_fps(self, key):
        """Press f5 to turn on/off displaying the framerate in the caption."""
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)

    def update(self, dt):
        self.current_time = pg.time.get_ticks()
        self.state.update(dt, self.current_time, self.keys)
        if self.show_fps:
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pg.display.set_caption(with_fps)

        if self.state.quit:
            self.done = True            
        if self.state.done:
            self.change_state() 

    def change_state(self):
        previous, self.state_name = self.state_name, self.state.next
        data = self.state.clear()
        self.state = self.state_dict[self.state_name]
        self.state.start(data, self.current_time)
        self.state.previous = previous

    def render(self):
        self.screen.fill(self.bg_color)
        self.state.render(self.screen)
        pg.display.update()

    def main_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            self.render()
            

class _State(object):
    """ Parent class for the game states. All states should inherint from it."""
    def __init__(self):
        self.quit = False
        self.done = False
        self.previous = None
        self.next = None
        self.data = {}
        self.star_time = 0.0
        self.current_time = 0.0

    def handle_events(self, event):
        pass

    def update(self, dt , current_time, keys):
        pass

    def render(self, surface):
        pass

    def clear(self):
        """ Retunr the persintant data, cleanup all changes. 
            For complex states this method should be overloaded"""
        self.done = False
        return self.data

    def start(self, data, star_time):
        self.data = data
        self.star_time = star_time