import os, time, math

from os.path import join, basename, exists, isdir
from point import Point

p1 = Point(0,0,0)
p2 = Point(1,0,1)
p3 = Point(2,-1,1)
p4 = Point(0,2,3)

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


def polar(r,angle):
	x = r * math.cos(angle)
	y = r * math.sin(angle)
	return Point(2*math.pi,x,y)

def calcMag(x,y):
	return math.sqrt(x*x + y*y)

def angle(u,v,w):
	x1 = v.x - u.x
	y1 = v.y - u.y
	x2 = w.x - v.x
	y2 = w.y - v.y

	dotproduct = x1*x2 + y1*y2
	mag1 = calcMag(x1,y1)
	mag2 = calcMag(x2,y2)
	pheta = dotproduct / (mag1*mag2)

	alpha = math.acos(pheta)
	return math.pi - alpha

def turn(u,v,w):
	x1 = v.x - u.x
	y1 = v.y - u.y

	x2 = w.x - v.x
	y2 = w.y - v.y

	zcomp = x1 * y2 - y1 * x2

	if zcomp > 0.0:
		return 'left'
	elif zcomp == 0.0:
		return 'collinear'
	else:
		return 'right'

def angularDisplacement(v,i,z): #v is a stack
	#print "angularDisplacement"
	#print "i: " + str(i)
	if i == 0:
		return 0
	else:
		#print v[i]
		if turn(z,v[i-1],v[i]) == 'left':
			return angularDisplacement(v,i-1,z) + angle(v[i-1],z,v[i])
		elif turn(z,v[i-1],v[i]) == 'right':
			return angularDisplacement(v,i-1,z) - angle(v[i-1],z,v[i]) 
		else:
			return angularDisplacement(v,i-1,z)

def theta():
	print "pheta"

def vispol(z,v,n,s,t):
	#vision point z in P 
	#vertices v = v0,v1,...,vn of P --- v0 satisfying assumption in sec2

	#output visibility polygon vertices s = s0,s1,...st, where s0 = v0 st = vn
	s[0] = v[0]
	i = 0
	t = 0
	ccw = None
	w = None
	if v[1].angularDisplacement >= v[0].angularDisplacement:
		upcase = 'advance'
	else:
		upcase = 'scan'
		ccw = True
		w = polar(99999999,0) #point with polar coordinates (infinity, @(v0))
	while upcase != 'finish':
		#print s
		if upcase == 'advance':
			s,t,i,upcase,ccw, w = advance(z,v,n,s,t,i,upcase,ccw,w)
		elif upcase == 'retard':
			s,t,i,upcase,ccw, w = retard(z,v,n,s,t,i,upcase,ccw,w)
		elif upcase =='scan':
			s,t,i,upcase = scan(z,v,n,s,t,i,upcase,ccw,w)
	return s

def advance(z,v,n,s,t,i,upcase,ccw,w):
	while upcase == 'advance':
		print s
		print 'advance'
		print i
		print 't: ' + str(t)
		if v[i+1].angularDisplacement <= 2*math.pi:
			i = i+1
			t = t+1
			s[t] = v[i]
			if i == n:
				upcase = 'finish'
			elif v[i+1].angularDisplacement < v[i].angularDisplacement:
				if turn(v[i-1], v[i], v[i+1]) == 'right':
					print 'hi'
					upcase = 'scan'
					ccw = True
					pheta = v[i].angularDisplacement
					while pheta >= 2*math.pi:
						pheta -= 2*math.pi
					w = polar(99999999, pheta) #point with polar coordinates (infinity, @(vi))
					#print "w"
					#print w
				elif turn(v[i-1], v[i], v[i+1]) == 'left':
					upcase = 'retard'
		else:
			if s[t].angularDisplacement < 2*math.pi:
				t = t+1
				s[t] = intersection(v[i],v[i+1],z,v[0])
			upcase = 'scan'
			ccw = False
			w = v[0]
		#print 'end advance' + str(i) + ' upcase = ' + upcase
	return s,t,i,upcase,ccw, w

def retard(z,v,n,s,t,i,upcase,ccw,w):
	while upcase == 'retard':
		print s
		print 'retard'
		print i
		j = 0
		for count in range(t-1,0, -1): 
			#scan backwards s[t-1] s[t-2]....s[0]
			if s[count].angularDisplacement < v[i+1].angularDisplacement and v[i+1].angularDisplacement <= s[count+1].angularDisplacement:
				print 'count ' + str(count)
				j = count
				break
			elif v[i+1].angularDisplacement <= s[count].angularDisplacement and s[count].angularDisplacement == s[count+1].angularDisplacement and intersects(v[i],v[i+1],s[count],s[count+1]):
				print 'count ' + str(count)
				j = count
				break
		if s[j].angularDisplacement < v[i+1].angularDisplacement:
			i = i+1
			t = j+1
			print 's[j]: ' + str(s[j])
			print 's[j+1]: ' + str(s[j+1])
			print 'v[i]: ' + str(v[i])
			s[t] = intersection(s[j],s[j+1],z,v[i])
			t = t+1
			s[t] = v[i]
			if i == n:
				upcase = 'finish'
			elif v[i+1].angularDisplacement >= v[i].angularDisplacement:
				if turn(v[i-1], v[i], v[i+1]) == 'right':
					upcase = 'advance'
			elif v[i+1].angularDisplacement > v[i].angularDisplacement:
				if turn(v[i-1], v[i], v[i+1]) == 'left':
					upcase = 'scan'
					ccw = False
					w = v[i]
					t = t-1
			else:
				t = t-1
		else:
			if v[i+1].angularDisplacement == s[j].angularDisplacement and v[i+2].angularDisplacement > v[i+1].angularDisplacement and turn(v[i], v[i+1], v[i+2]) == 'right':
				upcase = 'advance'
				i = i+1
				t = j+1
				s[t] = v[i]
			else:
				upcase = 'scan'
				t = j
				ccw = True
				w = intersection(v[i],v[i+1],s[j],s[j+1])
	return s,t,i,upcase,ccw, w

def scan(z,v,n,s,t,i,upcase,ccw,w):
	while upcase == 'scan':
		print s
		print 'scan'
		print i 
		i = i+1
		print 't: ' + str(t)
		alpha1 = v[i+1].angularDisplacement
		alpha2 = s[t].angularDisplacement
		print 's[t]: ' + str(alpha2)
		if ccw and alpha1 > alpha2 and s[t].angularDisplacement >= v[i].angularDisplacement:#angularDisplacement(v,i+1,z) > angularDisplacement(s,t,z):
			if intersects(v[i],v[i+1],s[t],w):
				s[t+1] = intersection(v[i],v[i+1],s[t],w)
				t = t+1
				upcase = 'advance'
		elif not ccw:
			if v[i+1].angularDisplacement <= s[t].angularDisplacement and s[t].angularDisplacement < v[i].angularDisplacement:
				if intersects(v[i],v[i+1],s[t],w):
					upcase = 'retard'
	return s,t,i,upcase

#print turn(p1,p2,p3)
#print angle(p1,p2,p3)

def runalgorithm(num):
	polygonPoints, guardPoints = polyToPoint(num)
	z = guardPoints[0]
	v = polygonPoints
	count = 0
	for point in v:
		alpha = angularDisplacement(v,count,z)
		point.set_alpha(alpha)
		v[count] = point
		count += 1
	#print "v0 angular displacement" 
	#print v[5].angularDisplacement
	v.append(v[0])
	#print v
	n = len(v)
	#print "n: " + str(n)
	s = v
	t = len(v)
	visiblePolygon = vispol(z,v,n,s,t)
	print visiblePolygon

runalgorithm(0)


