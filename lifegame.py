import numpy as np
from scipy import signal
import time
from tkinter import *
from os import system, name 

class lifegame:
	mask = np.ones((3,3), dtype=int)
	
	def __init__(self, aliveProp = 0.5):
		width = 30
		height = 30
		self.field = np.array(np.random.rand(height*width) + aliveProp, dtype=int).reshape(height, width)
		
	def printfield(self):
		print(self.field)
		
	def checkNeighbour(self):
		return signal.correlate2d(self.field,self.mask, mode="same", boundary="wrap")
		
	def nextGeneration(self):
		neighbourCount = self.checkNeighbour()
		# if neignbour == 2~3 and cell = 1, new cell = 1 
		# if neignbour == 3 && cell = 0, new cell = 1
		# => neignbour + cell == 3, new cell = 1, neighbour + cell == 4 && cell = 1, new cell = 1
		# new cell = ( neignbour + cell == 3 or (neighbour + cell == 4 && cell = 1) ) 
		self.field = ( neighbourCount == 3 ) + self.field * ( neighbourCount == 4 )
		

		
if __name__ == "__main__":
	starttime = time.time()
	newgame = lifegame();
	system('cls')
	newgame.printfield()
	for i in range(5):
		system('cls')
		newgame.nextGeneration()
		newgame.printfield()
	print("runtime:")
	print(time.time()-starttime)