import pygame as pg

import state
from .. import util

class MissionCompleteState(state._State):
    def __init__(self):
        super(MissionCompleteState, self).__init__()
        self.bg_color = (0,0,0)
        self.text_color = (255,255,255)
        self.duration = 3 #seg
        self.image = pg.Surface(util.SCREEN_SIZE)
        self.next = "Splash"
        self.title = "Mission Complete"
        self.titleSurface = self.make_title_surface()
        self.rect = self.titleSurface.get_rect()
        self.rect.center = util.SCREEN_RECT.center

    def make_title_surface(self):
        font = pg.font.Font(util.FONTS['west-england.regular'], 70)
        return font.render(self.title, False, self.text_color)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.done = True

    def render(self, surface):
        self.image.fill(self.bg_color)
        self.image.blit(self.titleSurface, self.rect)
        surface.blit(self.image, (0,0))