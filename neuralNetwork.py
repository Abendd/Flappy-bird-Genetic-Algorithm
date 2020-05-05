import numpy as np


class Brain:
	def __init__(self,n_i=None,n_h=None,n_o=None,brain=None,flag=False):
		if flag:
			self.n = brain.n
			self.W1 = brain.W1
			self.W2 = brain.W2

			self.b1 = brain.b1
			self.b2 = brain.b2
		else:
			self.n = n_i
			self.W1 = np.random.randn(n_h,n_i)*0.1
			self.W2 = np.random.randn(n_o,n_h)*0.1

			self.b1 = np.zeros(shape=(n_h,1))
			self.b2 = np.zeros(shape=(n_o,1))
	def sigmoid(self,input):
		return 1/(1+np.exp(-input))

	def predict(self,input):
		input = np.array(input)
		input.resize((self.n,1))
		z1 = np.dot(self.W1,input)+self.b1
		a1 = self.sigmoid(z1)
		z2 = np.dot(self.W2,a1)+self.b2
		a2 = self.sigmoid(z2)
		return a2
	