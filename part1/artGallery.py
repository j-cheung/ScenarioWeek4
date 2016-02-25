import os, time, math
"""
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
"""
from os.path import join, basename, exists, isdir
from decimal import *

from point import Point
from triangulation import Triangulation
from coloring import Coloring
import threading


INPUT_FILE_DIR = "input/"
OUTPUT_FILE_DIR = "output/"

class ArtGallery(object):

	def __init__(self, point):
		self._point = Point(point.id, point.x, point.y)
		#Array of points
		self._points = [point]
		#Array of tuples
		self._polygon = [(point.x, point.y)]
		self._triangulation = Triangulation(self._points)
		self._color = Coloring(self._points, self._triangulation)
		# for mult-tread preview
		self.lock = threading.RLock()
		self.Version = 0


	@staticmethod
	def readguardsfile(num):
		inputFileName = "guards"
		infilename = os.path.join(INPUT_FILE_DIR, inputFileName + '.pol')
		outfilename = os.path.join(INPUT_FILE_DIR, inputFileName + '.sol')
		with open(infilename, 'r') as f:
			polygons = []
			for i in range(0,30):
				line = f.readline()
				line = line.rstrip()
				while not line.startswith(':'):
					line = line.lstrip("0123456789");
				line = line.lstrip(': ')
				polygons.append(line)
			polygonVertices = []
			for polygon in polygons:
				s = polygon
				vertices = []
				tempStr = ''
				inTuple = False
				j = 0
				while j < len(s):
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
					j += 1
				polygonVertices.append(vertices)
			return polygonVertices[num]


	@staticmethod
	def polyToPoint(num):
		points = []
		i = 0
		polygonArr = (ArtGallery.readguardsfile(num))
		for pt in polygonArr:
			pt2 = pt.strip('()')
			pt3 = pt2.replace(",", "")
			x, y = pt3.split()
			getcontext().prec = 16
			point = Point(i, float(x), float(y))
			i += 1
			points.append(point)
		#print points
		return points


	#Functions from demo
	def _update(self):
		self._points.sort()
		self._polygon = []
		for p in self._points:
			self._polygon.append((p.x, p.y))
		#print self._polygon

	def get_polygon(self):
		with self.lock:
			return self._polygon

	def get_process_point(self):
		with self.lock:
			return self._point

	def get_points(self):
		with self.lock:
			return self._points
	
	def get_diagonals(self):
		with self.lock:
			return self._triangulation.get_diagonals()

	def get_min_color(self):
		with self.lock:
			return self._color.get_min_color()

	def is_guard(self, point):
		with self.lock:
			return point.color == self._color.get_min_color()
	#How nice!

	#Add a new point to the art gallery!
	def include(self, point):
		with self.lock:
			self._points.append(Point(point.id, point.x, point.y))
			self._update()
			triangulated = self._triangulation.process()
			if (triangulated):
				self._color.process()
			# version control due to refresh of the painter object
			self.Version += 1

def output_part1(guardsSolution):
	inputFileName = "guards"
	outfilename = os.path.join(OUTPUT_FILE_DIR, inputFileName + '.sol')
	with open(outfilename, 'w') as f:
		f.write('uakari\n')
		f.write('g3en4qh6rk9s518noj535r75p9\n')
		count = 1
		for polygon in guardsSolution:
			f.write(str(count))
			f.write(':\t')
			thatsolution = str(polygon)
			thatsolution = thatsolution.strip('[]')
			thatsolution = thatsolution.strip('\'')
			f.write(thatsolution)
			f.write('\n')
			count += 1

if __name__ == '__main__':
		#tmp = ArtGallery.load("input/guards.pol")
		solution = []        
		for count in range(0,30):
			tmp = ArtGallery.polyToPoint(count)
			g = ArtGallery(tmp.pop(0))
			for p in tmp:
				g.include(p)
			onesolution = []
			i=0
			for p in g.get_points():
				if g.is_guard(p):
					#print p, " GUARD!"
					onesolution.append((ArtGallery.readguardsfile(count))[i])
				i += 1
				#else:
					#print p
			#print count
			print str(count) + " " + str(len(onesolution))
			solution.append(onesolution)
		print solution
		output_part1(solution)

