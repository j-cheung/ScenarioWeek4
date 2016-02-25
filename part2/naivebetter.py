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
	xv = v2.x - v1.x
	yv = v2.y - v1.y

	xw = w2.x - w1.x
	yw = w2.y - w1.y
	#v: (xv1,yv1) + (xv,yv)t
	#w: (xw1,yw1) + (xw,yw)t
	t = -(yw * (v1.x - xw) / (xv*yw))
	intersectX = v1.x + (t * xv)
	intersectY = v1.y + (t * yv)

	return Point(0,intersectX,intersectY)

def intersects(v1,v2,w1,w2):
	xv = v2.x - v1.x
	yv = v2.y - v1.y
	xw = w2.x - w1.x
	yw = w2.y - w1.y
	if xv*yw == 0:
		return False
	intersectingP = intersection(v1,v2,w1,w2)
	if (intersectingP.x <= v2.x and intersectingP.x >= v1.x) or (intersectingP.x <= v1.x and intersectingP.x >= v2.x):
		if (intersectingP.y <= v2.y and intersectingP.y >= v1.y) or (intersectingP.y <= v1.y and intersectingP.x >= v2.y):
			if (intersectingP.x <= w2.x and intersectingP.x >= w1.x) or (intersectingP.x <= w1.x and intersectingP.x >= w2.x):
				if (intersectingP.y <= w2.y and intersectingP.y >= w1.y) or (intersectingP.y <= w1.y and intersectingP.x >= w2.y):
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
	#for each edge:
	for j in range(0,len(s)-1):
		edge = [s[j],s[j+1]]
		for vertex in edge:
			print 'vertex - ' + str(vertex)
			r = distance(guard,vertex)
			vispolPoint = vertex
			#theta = angle(vertex,guard,s[0])
			for i in range(0,len(s)-1):
				if intersects(guard,vertex,s[i],s[i+1]):
					#print 'hi'
					intersecting = intersection(guard,vertex,s[i],s[i+1])
					print 'intersecting - ' + str(intersecting)
					if distance(guard,intersecting) < r:
						print 'smaller distance - ' + str(distance(guard,intersecting))
						r = distance(guard,intersecting)
						vispolPoint = intersecting
			#vispolPoint = 
			print vispolPoint
			vispoly.append(vispolPoint)
	return vispoly
		# for each edge in polygon, find if line from guard to point(vertex) intersects edge
		# add intersection closest to guard to vispoly

def run_algorithm(num):
	polygon,guards = polyToPoint(num)
	print naive_better(guards[0],polygon)
	#print polygon
	#print guards
	#print 'distance - ' + str(distance(Point(0,2,0),Point(0,0,0)))


run_algorithm(0)




