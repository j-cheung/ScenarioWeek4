
class Point(tuple):

	def __new__(cls, num, x, y):
		return tuple.__new__(cls,(float(num), float(x), float(y)))

	def __init__(self, num, x, y):
		super(Point, self).__init__(num, x, y)
		self.id = float(num)
		self.x = float(x)
		self.y = float(y)
		self.color = 0

	def __repr__(self):
		return "(%s, %s)" % (self.x, self.y)

	def get_pos(self):
		return (self.x, self.y)