
from point import Point
from side import Side

class Triangle(object):

	def __init__(self, point0, point1, point2):

		self.point0 = point0
		self.point1 = point1
		self.point2 = point2

	def __repr__(self):
        return "Triangle[(%s, %s), (%s, %s), (%s, %s)]" % (self.point0.x, self.point0.y, self.point1.x, self.point1.y, self.point2.x, self.point2.y)

    def __iter__(self):
        yield self.point0
        yield self.point1
        yield self.point2

    def sides(self):
    	return (Side(self.point0, self.point1), Side(self.point1, self.point2), Side(self.point2, self.point0))

    def opposite(self, side):
    	if self.point0 == side.point0:
    		if self.point1 == side.point1:
    			return self.point2
    		else:
    			return self.point1
    	elif self.point0 == side.point1:
    		if self.point1 == side.point0:
    			return self.point2
    		else:
    			return self.point1
    	return self.point0
