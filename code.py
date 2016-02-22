import os, time, math

from os.path import join, basename, exists, isdir

INPUT_FILE_DIR = "input/"
OUTPUT_FILE_DIR = "output/"

def readfile():
	inputFileName = "guards"
	infilename = os.path.join(INPUT_FILE_DIR, inputFileName + '.pol')
	outfilename = os.path.join(INPUT_FILE_DIR, inputFileName + '.sol')
	with open(infilename, 'r') as f:
		polygons = []
		for i in range(0,29):
			line = f.readline()
			line = line.rstrip()
			while not line.startswith(':'):
				line = line.lstrip("0123456789");
			line = line.lstrip(': ')

			polygons.append(line)
		
		s = polygons[0]
		print s
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
		print vertices
		#print s
		#print polygons[1] 

readfile()