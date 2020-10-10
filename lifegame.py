import numpy as np
from scipy import signal
import time
from tkinter import *
from os import system, name 

class game(object):
	mask = np.ones((3,3), dtype=int)
	
	def __init__(self, height, width, aliveProp = 0.5):
		#self.field = np.array(np.random.rand(height*width) + aliveProp, dtype=int).reshape(height, width)
		self.field = np.array(np.zeros(height*width) + aliveProp, dtype=int).reshape(height, width)

	def checkNeighbour(self):
		return signal.correlate2d(self.field,self.mask, mode="same", boundary="fill")

	def nextGeneration(self):
		neighbourCount = self.checkNeighbour()
		# if neignbour == 2~3 and cell = 1, new cell = 1 
		# if neignbour == 3 && cell = 0, new cell = 1
		# => neignbour + cell == 3, new cell = 1, neighbour + cell == 4 && cell = 1, new cell = 1
		# new cell = ( neignbour + cell == 3 or (neighbour + cell == 4 && cell = 1) ) 
		self.field = ( neighbourCount == 3 ) + self.field * ( neighbourCount == 4 )

class gameCanvas(game):

	def __init__(self,height,width):
		super().__init__(height,width)
		self.width = width
		self.height = height
		self.window = Tk()
		self.canvas = Canvas(self.window, width=width*10, height=height*10, bg="black")
		self.canvas.pack()
		self.grids = self.initGrids()
		self.gridLines = self.createGridLines()
		self.canvas.bind("<Button 1>",self.clickGrid)
		self.window.bind('<Key>',self.enter)
		self.updateGrids()
		self.working = False

	def clickGrid(self,event):
		x = int(event.x / 10)
		y = int(event.y / 10)
		self.field[y][x] = (self.field[y][x] + 1) % 2
		self.canvas.itemconfig(self.grids[y][x],fill = "red" if self.field[y][x] else "black")

	def enter(self,event):
		if (event.keycode == 13):
			self.working = not(self.working)
			if (self.working):
				self.loop()
			else:
				self.stop()
	
	def loop(self):
		self.nextGeneration()
		self.updateGrids()
		self.beginID = self.window.after(20,self.loop)
	
	def stop(self):
		self.window.after_cancel(self.beginID)
		
	def mainloop(self):
		self.window.mainloop()

	def createGridLines(self):
		output = []
		for i in range(0,self.width*10,10):
			output.append(self.canvas.create_line(i, 0, i, self.height*10, tag='grid_line', fill="green"))
		for i in range(0,self.height*10,10):
			output.append(self.canvas.create_line(0, i, self.width*10, i, tag='grid_line', fill="green"))
		return output

	def initGrids(self):
		output = []
		for i in range(self.height):
			currentLine = []
			for j in range(self.width):
				currentLine.append(self.canvas.create_rectangle(j*10,i*10,(j+1)*10,(i+1)*10,fill="black"))	
			output.append(currentLine)
		return output

	def updateGrids(self):
		for i in range(self.height):
			for j in range(self.width):
				if self.field[i][j] == 1:
					self.canvas.itemconfig(self.grids[i][j],fill="red")
				if self.field[i][j] == 0:
					self.canvas.itemconfig(self.grids[i][j],fill="black")

	def renew(self):
		self.canvas.update()

		
if __name__ == "__main__":
	starttime = time.time()
	newgame = gameCanvas(30,50)
	newgame.mainloop()