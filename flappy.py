import pygame
import random
import math
from pygame.locals import *
import numpy as np
from bird import Bird
from pipe import Pipe
from ga import *

clock = pygame.time.Clock()

class App:
	width = 500
	height = 450
	def __init__(self,population):
		self.background_image = pygame.image.load("background.png")
		self.background_image = pygame.transform.scale(self.background_image, (500, 450))
		self.bird = []
		self.oldBird=[]
		self.population = population
		self.pipes = []
		self.win = None
		self.running = True
		self.interval = 0
		self.j=0
		self.remaining = 0
		self.gen =0
		self.highestScore=0
	def on_init(self):
		pygame.init()
		self.win = pygame.display.set_mode((self.width,self.height))
		
	def on_render(self):
		self.win.blit(self.background_image, [0, 0])
		for i in self.bird:
			i.update()
			i.draw(self.win)
		for pipe in self.pipes:
			pipe.draw(self.win)
			pipe.update()
		if len(self.pipes)>0:
			if self.pipes[0].isOver():
				self.pipes.remove(self.pipes[0])

		pygame.display.update()
		clock.tick(60)

	def on_cleanup(self):
		pygame.quit()
	
	def isHit(self,bird,closest_pipe):
		return (((bird.x>closest_pipe.x and bird.x<closest_pipe.x+closest_pipe.pipeWidth) or (bird.x+35>closest_pipe.x)) and ((bird.y<closest_pipe.height) or (bird.y+25>closest_pipe.height+closest_pipe.gap))) or bird.y+25>490
	
	def closest_pipe(self):
		for i in self.pipes:
			if i.x+i.pipeWidth<self.bird[0].x:
				continue
			else:
				return i
	def best_score(self):
		m = 0
		if len(self.oldBird)!=0:
			for i in self.oldBird:
				if i.score>m:
					m = i.score
		if m>self.highestScore:
			self.highestScore=m
		return m

	def nextGeneration(self):
		self.resetState()
		if len(self.oldBird)==0:
			for i in range(self.population):
				self.bird.append(Bird())
		else:
			self.normalize_fitness()
			for i in range(self.population):
				self.bird.append(self.poolSelection())
		print("Generation:",self.gen,"highest score of current gen:",self.best_score(),"highestScore:",self.highestScore)
		self.gen+=1
		self.oldBird=[]

	def resetState(self):
		self.bird =[]
		self.pipes=[]
		self.interval=0


	def normalize_fitness(self):
		total = 0
		for i in self.oldBird:
			total+=i.score 

		for i in self.oldBird:
			i.fitness = i.score/total
			


	def poolSelection(self):
		m = 0

		for i in self.oldBird:
			if i.fitness>m:
				b = i
		child = Bird(b.brain,flag=True)
		child.mutate()
		return child
 		
	def on_execute(self):
		self.on_init()
		while(self.running):
		
			if len(self.bird)==0:
				self.nextGeneration()
				self.remaining = self.population

			if self.interval%100==0:
				self.pipes.append(Pipe())
			keys = pygame.key.get_pressed()
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					self.running = False


			closest_pipe = self.closest_pipe()
			self.remaining = len(self.bird)
			while self.j<self.remaining:
				self.bird[self.j].think(closest_pipe)
				if self.isHit(self.bird[self.j],closest_pipe):
					self.oldBird.append(self.bird[self.j])
					self.bird.remove(self.bird[self.j])
					self.remaining-=1
				self.j+=1
			self.j = 0
			self.interval+=1
			self.on_render()
		self.on_cleanup()


theApp = App(200)
theApp.on_execute()
