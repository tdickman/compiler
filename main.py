import sys
from scanner import *

def main():
	# Get the filename from the command line parameters
	if (len(sys.argv) > 1):
		fileName = sys.argv[1]
	else:
		print "Usage: python main.py infile.c"
		sys.exit(0)
	# Initialize parser
	p = Parser(fileName)
	p.parse()

if __name__ == "__main__":
	main()
