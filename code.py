import os, time, math
import plotly.plotly as py
import plotly.graph_objs as go



from os.path import join, basename, exists, isdir

INPUT_FILE_DIR = "input/"
OUTPUT_FILE_DIR = "output/"


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
		#guardsPolygonVertices.append(polygonVertices)
		#print s
		#print polygons[1] 

guardsPolygonVertices =  readguardsfile()
a =  guardsPolygonVertices[29]

def getXYlists(singlePolygon): #takes in one list of vertices for a selected polygon
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
	return Xlist, Ylist

aXlist, aYlist = getXYlists(a)

trace1 = go.Scatter(
    x=aXlist,
    y=aYlist,
    fill='tozeroy'
)

data = [trace1]
plot_url = py.plot(data, filename='Area')



print aXlist
