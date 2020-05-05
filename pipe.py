import pygame
from pygame.locals import *
import random

class Pipe:
	
	def __init__(self):
		self.pipe = pygame.image.load("./pipe-green.png")
		self.invertedPipe = pygame.transform.rotate(
                self.pipe.convert_alpha(), 180)
		self.invertedPipe = pygame.transform.scale(self.invertedPipe, (self.invertedPipe.get_size()[0], 450))
		self.invertedHeight = self.invertedPipe.get_size()[1]
		self.height = random.randint(50,300)
		self.gap = 100
		self.x = 450
		self.pipeWidth=50	

	def draw(self,win):
		win.blit(self.invertedPipe,(self.x,500-(500-self.gap-self.height)-self.gap-self.invertedHeight,self.pipeWidth,10))
		win.blit(self.pipe,(self.x,self.height+self.gap,self.pipeWidth,500-self.gap-self.height))
		#pygame.draw.rect(win,(0,0,255),(self.x,0,self.pipeWidth,self.height))
		#pygame.draw.rect(win,(0,0,255),(self.x,self.height+self.gap,self.pipeWidth,500-self.gap-self.height))
	def isOver(self):
		return self.x+self.pipeWidth<0

	def update(self):
		self.x-=3

