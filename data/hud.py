import pygame as pg

import util

class HUD(object):
	"""docstring for HUD"""
	def __init__(self):
		self.image = pg.Surface((50,50))
		self.rect = self.image.get_rect()
		self.font = pg.font.Font(util.FONTS['west-england.regular'], 20)
		self.hp = self.font.render('', False, (255,255,255))
		self.hp_rect = self.hp.get_rect(center=self.rect.center)

	def update(self, player):
		self.hp = self.font.render(str(player.hp), False, (255,255,255))
		self.hp_rect = self.hp.get_rect(center=self.rect.center)
		
	def render(self, surface):
		self.image.fill((0,0,0))
		pg.draw.rect(self.image, (255,255,255), self.rect, 5)
		self.image.blit(self.hp, self.hp_rect)
		return surface.blit(self.image, (16,16))