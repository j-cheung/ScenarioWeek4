
class Side(tuple):

	def __new__(cls, point0, point1):
		if (point0 > point1):
			temp = point0
			point0 = point1
			point1 = temp
		return tuple.__new__(cls, (point0, point1))

	def __init__(self, point0, point1):
		if (point0 > point1):
			temp = point0
			point0 = point1
			point1 = temp
		super(Side, self).__init__(point0, point1)
		self.point0 = point0
		self.point1 = point1

	def __repr__(self):
		return "Side(%s - %s)" % (self.point0,point1)
