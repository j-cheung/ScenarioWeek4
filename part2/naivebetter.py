import os, time, math

from os.path import join, basename, exists, isdir
from point import Point



INPUT_FILE_DIR = "../input/"
OUTPUT_FILE_DIR = "../output/"

def readcheckfile(num):
	inputFileName = "check"
	infilename = os.path.join(INPUT_FILE_DIR, inputFileName + '.pol')
	with open(infilename, 'r') as f:
		polygons = []
		for i in range(0,20):
			line = f.readline()
			line = line.rstrip()
			while not line.startswith(':'):
				line = line.lstrip("0123456789");
			line = line.lstrip(': ')
			polygons.append(line)
		polygonVertices = []
		guardCoordinates = []
		for polygon in polygons:
			s = polygon
			vertices = []
			guards = []
			tempStr = ''
			inTuple = False
			j = 0
			while j < len(s): #polygon vertices
				if s[j] == '(':
					inTuple = True
					tempStr += s[j]
				elif s[j] == ')':
					tempStr += s[j]
					vertices.append(tempStr)
					inTuple = False
					tempStr = ''
				elif inTuple:
					tempStr += s[j]
				elif s[j] == ';':
					break
				j += 1
			inTuple = False
			while j < len(s): #guard coordinates
				if s[j] == '(':
					inTuple = True
					tempStr += s[j]
				elif s[j] == ')':
					tempStr += s[j]
					guards.append(tempStr)
					inTuple = False
					tempStr = ''
				elif inTuple:
					tempStr += s[j]
				j += 1
			polygonVertices.append(vertices)
			guardCoordinates.append(guards)

		return polygonVertices[num], guardCoordinates[num]

def polyToPoint(num):
		polygonPoints = []
		guardPoints = []
		i = 0
		polygonArr,guardsArr = readcheckfile(num)
		for pt in polygonArr:
			pt2 = pt.strip('()')
			pt3 = pt2.replace(",", "")
			x, y = pt3.split()
			point = Point(i, float(x), float(y))
			i += 1
			polygonPoints.append(point)
		for pt in guardsArr:
			pt2 = pt.strip('()')
			pt3 = pt2.replace(",", "")
			x, y = pt3.split()
			point = Point(i, float(x), float(y))
			i += 1
			guardPoints.append(point)
		#print points
		return polygonPoints,guardPoints

def intersection(v1,v2,w1,w2):
	#v1,v2 : points of first vector
	#w1,w2 : points of second vector
	
	intersectX = ((v1.x * v2.y - v1.y * v2.x)*(w1.x - w2.x) - (v1.x - v2.x)*(w1.x * w2.y - w1.y * w2.x)) / ((v1.x - v2.x)*(w1.y - w2.y) - (v1.y - v2.y)*(w1.x - w2.x))
	intersectY = ((v1.x * v2.y - v1.y * v2.x)*(w1.y - w2.y) - (v1.y - v2.y)*(w1.x * w2.y - w1.y * w2.x)) / ((v1.x - v2.x)*(w1.y - w2.y) - (v1.y - v2.y)*(w1.x - w2.x))

	return Point(0,intersectX,intersectY)

def parallel(v1,v2,w1,w2):
	xv = v2.x - v1.x
	yv = v2.y - v1.y
	xw = w2.x - w1.x
	yw = w2.y - w1.y
	if (xv*yw - xw*yv)== 0: #parallel
		return True

def intersects(v1,v2,w1,w2):
	
	if parallel(v1,v2,w1,w2):
		return False
	intersectingP = intersection(v1,v2,w1,w2)
	if (intersectingP.x <= v2.x and intersectingP.x >= v1.x) or (intersectingP.x <= v1.x and intersectingP.x >= v2.x):
		if (intersectingP.y <= v2.y and intersectingP.y >= v1.y) or (intersectingP.y <= v1.y and intersectingP.y >= v2.y):
			if (intersectingP.x <= w2.x and intersectingP.x >= w1.x) or (intersectingP.x <= w1.x and intersectingP.x >= w2.x):
				if (intersectingP.y <= w2.y and intersectingP.y >= w1.y) or (intersectingP.y <= w1.y and intersectingP.y >= w2.y):
					return True
	return False

def collinear(a,b,c,d):
	
	if parallel(a,b,c,d) and parallel(a,b,a,c):
		return True
	return False

def distance(a,b):
	xdiff = b.x - a.x
	ydiff = b.y - a.y

	return math.sqrt(xdiff*xdiff + ydiff*ydiff)

def angle(target,initial,p_ref):
	#p1: target point
	#p2: initial point
	#p_ref: reference point
	dotproduct = (target.x-initial.x)*(p_ref.x-initial.x) + (target.y-initial.y)*(p_ref.y-initial.y)
	magA = distance(target,initial)
	magB = distance(p_ref,initial)
	if magA == 0 or magB == 0:
		return 0
	#print 'hi'
	cos = dotproduct / (magA*magB)
	if cos > 1 and cos <= 1.00000000001:
		cos = 1
	#print cos <= 1.0		
	return math.acos(cos)

def polar(r,angle,guard,p_ref):
	x = r * math.cos(angle)
	y = r * math.sin(angle)
	horizontal_end = Point(0,99999,guard.y)
	prefAngle = angle(horizontal_end,guard,p_ref)
	return Point(0,x,y)

def naive_better(guard,s):
	vispoly = []
	s.append(s[0])
	for j in range(0,len(s)-1): #each edge in polygon
		edge = [s[j],s[j+1]]
		for vertex in edge:
			r = distance(guard,vertex)
			vispolPoint = vertex
			#print 'vertex - ' + str(vertex)
			#print 'guard - ' + str(guard)
			#theta = angle(vertex,guard,s[0])
			#print 'angle - ' + str(theta)
			for i in range(0,len(s)-1): #each edge in polygon
				#print 'guard - ' + str(guard)
				if intersects(guard,vertex,s[i],s[i+1]):
					#print 'hi'
					intersecting = intersection(guard,vertex,s[i],s[i+1])
					if distance(guard,intersecting) < r:
						print 'guard - ' + str(guard)
						print 'vertex - ' + str(vertex)
						print 'edge - ' + str([s[i],s[i+1]])
						print 'intersecting - ' + str(intersecting)
						print 'smaller distance - ' + str(distance(guard,intersecting))
						r = distance(guard,intersecting)
						vispolPoint = intersecting
				#print 'temp vispolPoint - ' + str(vispolPoint)

			#vispolPoint = 
			#print 'final vispolPoint - ' + str(vispolPoint)
			vispoly.append(vispolPoint)
	return vispoly
		# for each edge in polygon, find if line from guard to point(vertex) intersects edge
		# add intersection closest to guard to vispoly

def point_in_poly(x,y,strlist):
	xl, yl = get_polygon_XYlists(strlist)
	xl.pop()
	yl.pop()
	poly = zip(xl, yl)
	
	n = len(poly)
	inside = False
	p1x ,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if y > min(p1y,p2y): 
			if y <= max(p1y,p2y): #if y is in between p1y and p2y
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xints = (y-p1y)*(p2x-p1x)/(p2y-p1y) + p1x
					if p1x == p2x or x <= xints:
						inside = not inside
		p1x,p1y = p2x,p2y
	return inside

def distance2(x1,y1,x2,y2):
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def is_between(x1,y1,x,y,x2,y2):
	return distance2(x1,y1,x,y) + distance2(x,y,x2,y2) == distance2(x1,y1,x2,y2)


def pointOnBorder1(x,y,strlist):
	xl, yl = get_polygon_XYlists(strlist)
	xl.pop()
	yl.pop()
	poly = zip(xl, yl)
	n = len(poly)
	for i in range(n):
		x1,y1 = poly[i]
		x2,y2 = poly[(i + 1) % n]
		if is_between(x1,y1,x,y,x2,y2) == True:
			return True
	return False

def isort(A):
	
	for i in range(1,len(A)):
		x = A[i]
		j = i - 1
		while j >= 0 and A[j].angularDisplacement > x.angularDisplacement:
			A[j+1] = A[j]
			j = j - 1
		A[j+1] = x
	return A

def perpendicular(v1,v2,w1,w2):
	dotproduct = (v2.x - v1.x)*(w2.x - w1.x) + (v2.y - v1.y)*(w2.y - w1.y)
	if dotproduct == 0:
		return True
	return False

def my_naive_better(select_guard,s):
	vispoly = []
	s.append(s[0])
	for vertex in s:
		print 'vertex - ' + str(vertex)
		vispolPoint = vertex
		for i in range(0,len(s)-1):
			if collinear(select_guard,vertex,s[i],s[i+1]):
				print 'collinear'
				vispolPoint = vertex
			elif intersects(select_guard,vertex,s[i],s[i+1]):
				intersecting = intersection(select_guard,vertex,s[i],s[i+1])

				#if intersecting point is on end of edge and intersecting angle is 90 then ignore

				if(intersecting.x == s[i].x and intersecting.y == s[i].y) or (intersecting.x == s[i+1].x and intersecting.y == s[i+1].y):
					if intersecting.x == s[i].x and intersecting.y == s[i].y:
						if perpendicular(select_guard,vertex,s[i],s[i+1]):
							break
						else:
							if intersecting.x != select_guard.x or intersecting.y != select_guard.y:
								if distance(intersecting,select_guard) < distance(vispolPoint,select_guard):
									vispolPoint = intersecting

				else:
					if intersecting.x != select_guard.x or intersecting.y != select_guard.y:
						if distance(intersecting,select_guard) < distance(vispolPoint,select_guard):
							vispolPoint = intersecting
		midpoint_x = (select_guard.x + vispolPoint.x) / 2
		midpoint_y = (select_guard.y + vispolPoint.y) / 2
		if not point_in_poly(midpoint_x,midpoint_y,s) and not pointOnBorder1(midpoint_x,midpoint_y,s):
			vispolPoint = select_guard

		'''quartile1_x = (select_guard.x + vispolPoint.x) / 4
		quartile1_y = (select_guard.y + vispolPoint.y) / 4


		quartile3_x = 3 * (select_guard.x + vispolPoint.x) / 4
		quartile3_y = 3 * (select_guard.y + vispolPoint.y) / 4

		if not point_in_poly(quartile1_x,quartile1_y,s) and not pointOnBorder1(quartile1_x,quartile1_y,s):
			if not point_in_poly(quartile3_x,quartile3_y,s) and not pointOnBorder1(quartile3_x,quartile3_y,s):
				vispolPoint = select_guard'''

		print 'vispolPoint - ' + str(vispolPoint)
		vispoly.append(vispolPoint)
#extend
	extendedvispol = []
	for vertex in vispoly:
		extendedvispol.append(vertex)
	for vertex in vispoly:
		vispolPoint = vertex
		candidates = []
		for i in range(0,len(s)-1):
			if collinear(select_guard,vertex,s[i],s[i+1]) or parallel(select_guard,vertex,s[i],s[i+1]):
				#vispolPoint = vertex
				break
			intersecting = intersection(select_guard,vertex,s[i],s[i+1])
			#if not (intersecting.x == s[i].x and intersecting.y == s[i].y) or (intersecting.x == s[i+1].x and intersecting.y == s[i+1].y):
			if intersecting.x != select_guard.x or intersecting.y != select_guard.y:
				if distance(intersecting,select_guard) > distance(vispolPoint,select_guard):
					if pointOnBorder1(intersecting.x,intersecting.y,s):
						candidate_point = Point(distance(intersecting,select_guard),intersecting.x,intersecting.y)
						candidates.append(candidate_point)
		if(len(candidates)>0):
			candidates = isort(candidates)
			
			for candidate_point in candidates:
				midpoint_x = (candidate_point.x + vispolPoint.x) / 2
				midpoint_y = (candidate_point.y + vispolPoint.y) / 2
				if point_in_poly(midpoint_x,midpoint_y,s) or pointOnBorder1(midpoint_x,midpoint_y,s): #line from next closest to current closest point is in polygon
					
					vispolPoint = candidate_point
				else:
					break
		extendedvispol.append(vispolPoint)

	
	extendedvispol =  sort_vispoly_angle(select_guard,extendedvispol)
	return vispoly

def sort_vispoly_angle(select_guard,vispoly):
	#print vispoly
	for vertex in vispoly:
		angle = math.atan2(vertex.y - select_guard.y, vertex.x - select_guard.x)
		if angle < 0 and angle >= (-math.pi):
			angle += 2*math.pi
		vertex.angularDisplacement = angle
	vispoly = isort(vispoly)
	distance_vispoly = []
	"""for vertex in vispoly:
					distance = distance(select_guard,vertex)
					sameangle = []
			
					if distance == 0
						break"""

	return vispoly
	#print vispoly

def sort_vispoloy_edge(vispoly,s):
	finalsorted = []
	for i in range(0,len(s)-1):
		temp = []


def get_polygon_XYlists_2(singlePolygon): #takes in one list of vertices for a selected polygon
	listLength = len(singlePolygon)
	Xlist = []
	Ylist = []
	for vertice in singlePolygon:
		coordinates = vertice.strip('()')
		coordinates = coordinates.split(',')
		x = coordinates[0]
		x = float(x)
		y = coordinates[1]
		y = float(y)
		Xlist.append(x)
		Ylist.append(y)
	firstVertice = singlePolygon[0]
	coordinates = firstVertice.strip('()')
	coordinates = coordinates.split(',')
	x = coordinates[0]
	x = float(x)
	y = coordinates[1]
	y = float(y)
	Xlist.append(x)
	Ylist.append(y)
	return Xlist, Ylist

def get_polygon_XYlists(singlePolygon): #takes in one list of vertices for a selected polygon
	listLength = len(singlePolygon)
	Xlist = []
	Ylist = []
	
	for vertice in singlePolygon:
		x = vertice.x
		y = vertice.y
		Xlist.append(x)
		Ylist.append(y)
	firstVertex = singlePolygon[0]
	firstVertex_x = firstVertex.x
	firstVertex_y = firstVertex.y
	Xlist.append(firstVertex_x)
	Ylist.append(firstVertex_y)
	return Xlist, Ylist

def get_guards_XYlists(guardList): #takes in one list of vertices for a selected polygon
	listLength = len(guardList)
	Xlist = []
	Ylist = []
	
	for vertice in guardList:
		x = vertice.x
		y = vertice.y
		Xlist.append(x)
		Ylist.append(y)
	return Xlist, Ylist

def plotcheck(initPolygon,visPolygonList,guards):
	import plotly
	import plotly.plotly as py
	import plotly.graph_objs as go
	from plotly.graph_objs import Scatter, Layout
	initpolXlist, initpolYlist = get_polygon_XYlists(initPolygon)
	guardXlist, guardYlist = get_guards_XYlists(guards)
	data = [Scatter(x=initpolXlist, y=initpolYlist, fill='tozeroy'), Scatter(x=guardXlist, y=guardYlist, mode = 'markers')]
	for visPolygon in visPolygonList:
		vispolXlist, vispolYlist = get_polygon_XYlists(visPolygon)
		trace = Scatter(x=vispolXlist, y=vispolYlist, mode = 'markers')
		data.append(trace)
	plotly.offline.plot(data)



def run_algorithm(num):
	polygon,guards = polyToPoint(num)
	#polygon,guards = readcheckfile(num)
	allvispoly = []
	guards = [guards[1]]
	
	for guard in guards:
		vispoly =  my_naive_better(guard,polygon)
		allvispoly.append(vispoly)
	
	#vispoly = my_naive_better(guards[1],polygon)
	#allvispoly.append(vispoly)
	#print polygon
	#print vispoly
	#print guards
	plotcheck(polygon,allvispoly,guards)
	#print polygon
	#print point_in_poly(3,2.1,polygon)
	

run_algorithm(6)




