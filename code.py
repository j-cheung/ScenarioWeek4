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
		for j in polygons:
			print j + '\n' 

readfile()