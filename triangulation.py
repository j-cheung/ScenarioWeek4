
from point import Point
from side import Side
from triangle import Triangle

class Triangulation(object):

    EPSILON = 0.0000000001

	def __init__(self, points):
		self.polygon = points
		self.clean()

	def clean(self):
		self.diagonals = {}
		self.sides = {}
		seld.start = None

	def addDiagonal(self, triangle):
		#identity
		diagonal = Side(triangle.point0, triangle.point2)
		#map the triangulation 
		self.diagonals[diagonal] = triangle
		self.addTriangle(triangle)

	def addTriangle(self, triangle):
		if self.start is None: self.start = triangle
        # each side of each triangle can be related to:
        # only one triangle (this side is part of original polygon) 
        # or two triangles (this side is a diagonal, created by triangulation)
        # map each side and correlated triangles
		for side in triangle.sides():
			tt = self.sides.get(side)
			# side already mapped
			if tt:
				# add this new correlated triangle (this side is a diagonal)
				self.sides[side] = (tt[0], triangle)
			else:
				# this side has just appeared. it can be a diagonal, 
                # but its opposite has not been triangulated yet
                self.sides[side] = (triangle, None)

    def get_start(self):
    	#return the first triangle cretated in the last triangulation
        #return self._triangles[0]
    	return self.start

    def get_diagonals(self):
    	return self.diagonals.keys()

    def get_neighbours(self, triangle):
    	neighbours = []
    	for side in triangle.sides():
    		neighbour = self.get_opposite(triangle, side)
    		if neighbour:
    			neighbours.append(neighbour)
    	return neighbours

    def get_opposite(self, triangle, side):    
    	tt = self.sides.get(side)
    	if tt: 
    		if tt[0] != triangle:
    			return tt[0]
    		elif tt[1]:
    			return tt[1]
    	return None


    def _set_indexes(self, v, n_points):
        """ Set indexes for triangulation based on v parameter """

        u = v
        if u >= n_points:
            u = 0

        v = u + 1
        if v >= n_points:
            v = 0

        w = v + 1
        if w >= n_points:
            w = 0

        return u, v, w

    def run(self):
    	# clear the current triangulation
        self.clean()
        n_points = len(self.polygon)
        # Minimum number of polygon to compose a triangle
        if n_points < 3:
            return False

        tmp_points = self.polygon[:]
        # reverse if not clockwise orientation
        if self.area() < 0.0:
        	tmp_points.reverse()

        # controls the current triangle points inside the while statement
        v = n_points - 1
        attempts = (n_points + 3)
        while n_points > 3:  
        	if not attempts:
        		self.clean()
        		return False
        	attempts -= 1 

            # start triangulation from the last triangulation point
            # this is best in some cases (e.x. concave polygon)
            # and worst in others (e.x. polygon with many inverses corners)...
            #last_mark = v
            u, v, w = self._set_indexes(v, n_points)

            # Creates a Triangle object with three consecutives Point objects
            triangle = Triangle(tmp_points[u], tmp_points[v], tmp_points[w])

            # check if this triangle can be cutted (snipped)
            if self._snip(tmp_points, triangle):
                # add current triangle to triangulation
                self.addDiagonal(triangle) 
                # remove triangle from polygon
                tmp_points.remove(tmp_points[v])  
                #v = last_mark # see above
                # adjust the loop controls
                n_points -= 1
                attempts = (n_points + 3)

        # add last triangle to triangulation
        triangle = Triangle(tmp_points[0], tmp_points[1], tmp_points[2])
        self.addTriangle(triangle)
        del tmp_points
        return True

    def _is_inside(self, point, triangle):
    	ax, ay = triangle.point2.x - triangle.point1.x, triangle.point2.y - triangle.point1.y
    	bx, by = triangle.point0.x - triangle.point2.x, triangle.point0.y - triangle.point2.y
    	cx, cy = triangle.point1.x - triangle.point0.x, triangle.point1.y - triangle.point0.y    	    	

        apx, apy = point.x - triangle.point0.x, point.y - triangle.point0.y
        bpx, bpy = point.x - triangle.point1.x, point.y - triangle.point1.y
        cpx, cpy = point.x - triangle.point2.x, point.y - triangle.point2.y

        a_cross = ax*bpy - ay*bpx
        b_cross = bx*cpy - by*cpx
        c_cross = cx*apy - cy*apx

        return a_cross >= 0 and b_cross >= 0 and c_cross >= 0

    def _snip(self, points, triangle):
        oppos = (triangle.point1.x - triangle.point0.x) * (triangle.point2.y - triangle.point0.y) 
        adjac = (triangle.point1.y - triangle.point0.y) * (triangle.point2.x - triangle.point0.x)

        # the triangle makes a inverse corner (open corner)?
        if self.EPSILON > (oppos - adjac):
        	# if so, then this triangle isn't a ear of polygon...
        	return False

        if point in points:
        	if point not in triangle and self._is_inside(point, triangle):
        		return False
        return True

    def area(self):
        size = len(self.polygon)
        area = 0.0
        i0 = size -1
        i1 = 0
        while i1 < size:
            area += self.polygon[i0].x * self.polygon[i1].y - \
                    self.polygon[i0].y * self.polygon[i1].x
            i0 = i1 
            i1 += 1
        return (area / 2)        









