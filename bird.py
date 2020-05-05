import pygame
from pygame.locals import *
from neuralNetwork import  Brain
import numpy as np
import random
class Bird:

	def __init__(self,brain=None,flag=False):
		self.character = pygame.image.load("./flappy.png")
		self.x = 20
		self.y = 400
		self.score=0
		self.isJumping = False
		self.isJump = False
		self.v = 4
		self.m = 2
		self.hitbox = [self.x,self.y,35,25]

		if flag:
			self.brain = Brain(brain=brain,flag=True)
		else:
			self.brain  = Brain(4,8,2)

		self.colorHitBox = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
		self.fitness = 0 
	def mutateFunc(self,x):
		if np.random.random()<0.1:
			return x + np.random.normal()*0.3
		else:
			return x

	def mutate(self):
		self.brain.W1 = self.mutateFunc(self.brain.W1)
		self.brain.W2 = self.mutateFunc(self.brain.W2)
		self.brain.b1 = self.mutateFunc(self.brain.b1)
		self.brain.b2 = self.mutateFunc(self.brain.b2)

	def jump(self):
		if self.isJump:
			self.isJumping = True
		else:
			self.isJump = True

	def draw(self,win):
		win.blit(self.character,(self.x,self.y))
		pygame.draw.rect(win,self.colorHitBox,self.hitbox,2)

	def think(self,closest_pipe):
		input = [self.x - closest_pipe.x,self.y-closest_pipe.height,closest_pipe.x,self.y-closest_pipe.height-closest_pipe.x,self.y-closest_pipe.gap,self.v]
		prediction = self.brain.predict(input)
		if prediction[1][0]>prediction[0][0]:
			self.jump()

	def update(self):
		self.score+=1
		if self.isJump:
			if self.isJumping:
				self.v=4
				self.isJumping=False
			if self.y<=0:
				self.v = 0
				self.y=1			
			if self.v>0:
				F = (0.3*self.m*self.v*self.v)
			else:
				F = -(0.3*self.m*self.v*self.v)

			if F<-10:
				F = -10
			self.y = self.y - F
			self.v = self.v - 1
			self.hitbox = [self.x,self.y,35,25]

			if self.y>500:
				self.y = 470
				self.v = 4
				self.isJump=False
				self.isJumping=False
		self.hitbox = [self.x,self.y,35,25]		



