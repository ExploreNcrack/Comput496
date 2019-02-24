import random 

class TranspositionTable(object):
	
	def __init__(self, size):
		self.size = size

	def initZobrist(self):
		outertable = []
		for i in range(self.size):
			innertable = []
			for j in range(self.size):
				innertable.append()