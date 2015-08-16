import pygame as pg

from ... import util
from .. import state
import menu

class MenuState(state._State):
    def __init__(self):
        super(MenuState, self).__init__()

    def set_options(self, options):     
        self.menu = menu.Menu(options, 50, 50)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            self.menu.handle_events(event.key)
            if event.key == pg.K_ESCAPE:
                self.quit = True

    def update(self, dt, current_time, keys):
        self.menu.update(dt)

    def render(self, surface):
        self.menu.render(surface)


class MainMenuState(MenuState):    

    def __init__(self):
        super(MainMenuState, self).__init__()
        self.options = [
            {"text":"PLAY", "nested": False, "activate": self.play},
            {"text":"CREDITS", "nested": False, "activate": self.credits},
            {"text":"QUIT", "nested": False, "activate": self.exit}
        ]
        self.set_options(self.options)

        util.music.play(util.bg_song, -1)        

    def start(self, data, start_time):
        self.set_options(self.options)

    def play(self):        
        self.done = True
        self.next = "Game"        

    def settings(self):
        self.done = True
        self.next = "Settings"

    def credits(self):
        self.done = True
        self.next = "Credits"

    def exit(self):
        self.quit = True