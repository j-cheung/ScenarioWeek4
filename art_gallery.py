
from point import Point
from triangulation import Triangulation
from coloring import Coloring
import threading
import os, time, math
from os.path import join, basename, exists, isdir

INPUT_FILE_DIR = "input/"
OUTPUT_FILE_NAME = "output/"

class ArtGallery(object):

	def __init__(self, point):
		self._point = Point(point.id, point.x, point.y)
		self._points = [point]
		self._polygon = [(point.x, point.y)]
		self._triangulation = Triangulation(self._points)
		self._color = Coloring(self._points, self._triangulation)

	def readguardsfile():
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

			return polygonVertices

	def _update(self):
		self._points.sort()
		self._polygon = []
		for p in self._points:
			self._polygon.append((p.x, p.y))

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
            
if __name__ == '__main__':
			        
	print ("Starting...")
	tmp = ArtGallery.readguardsfile()
	g = ArtGallery(tmp.pop(0))
	for p in tmp:
		g.include(p)
		        
	for p in g.get_points():
		if g.is_guard(p):
		    print (p, " GUARD!")
		else:
		    print (p)
		                
	print ("Min_color = " + str(g._color.get_min_color()))
	print ("color[0] = " + str(g._color.get_color_count(0)))
	print ("color[1] = " + str(g._color.get_color_count(1)))
	print ("color[2] = " + str(g._color.get_color_count(2)))
	print ("color[3] = " + str(g._color.get_color_count(3)))