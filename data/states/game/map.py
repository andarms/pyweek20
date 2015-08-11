import pygame as pg

class Map(object):
	"""docstring for Map"""
	def __init__(self, world):		
		self.world = world
		self.obstacles = self.make_obstacles()

