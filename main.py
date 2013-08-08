import sys
from parser import *

def main():
	# Get the filename from the command line parameters
	if (len(sys.argv) > 1):
		fileName = sys.argv[1]
		verbose = False
		if (len(sys.argv) > 2) and sys.argv[2] == "-v":
			verbose = True
	else:
		print "Usage: python main.py infile.c"
		sys.exit(0)
	# Initialize parser
	p = Parser(fileName, verbose)
	p.parse()

if __name__ == "__main__":
	main()
