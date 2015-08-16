import pygame as pg

import state
from .. import util
MSN = """HackerMan

Solo entry for Pyweek 20 "data, data, data!"

i hope that you can enjoy this little game 
made with much love and hard work.

By Adrian Manjarres @ANDarms
"""

FONT = pg.font.Font(util.FONTS['west-england.regular'], 25)
class CreditsState(state._State):
    def __init__(self):
        super(CreditsState, self).__init__()       
        self.msn = pg.sprite.Group()
        self.credits_msn = MSN
        self.generate_text()

    def generate_text(self):
        lines = self.credits_msn.split('\n')
        size = width, height = util.SCREEN.get_size()

        y = 50
        line_height = 40
        for line in lines:
            if line is not '':
                line_rendered = pg.sprite.Sprite(self.msn)
                l = FONT.render(line, 1, (255,255,255))
                rect = l.get_rect(centerx=width/2, centery=y+line_height)
                line_rendered.image = l
                line_rendered.rect = rect
            y += line_height

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            self.back()

    def back(self):
        self.done = True
        self.next = "MainMenu"

    def render(self, surface):
        self.msn.draw(surface)