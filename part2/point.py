from decimal import *

class Point(tuple):

	getcontext().prec = 16

	def __new__(cls, angularDisplacement, x, y):
		return tuple.__new__(cls,(float(angularDisplacement), float(x), float(y)))

	def __init__(self, angularDisplacement, x, y):
		super(Point, self).__init__(angularDisplacement, x, y)
		self.angularDisplacement = float(angularDisplacement)
		self.x = float(x)
		self.y = float(y)
		self.color = 0

	def __repr__(self):
		return "(%s, %s, %s)" % (self.angularDisplacement, self.x, self.y)

	def get_pos(self):
		return (self.x, self.y)

	def set_alpha(self, angularDisplacement):
		self.angularDisplacement = angularDisplacement