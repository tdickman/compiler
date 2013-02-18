import sys
from scanner import *

def main():
	# Get the filename from the command line parameters
	if (len(sys.argv) > 1):
		fileName = sys.argv[1]
	else:
		print "Usage: python main.py infile.c"
		sys.exit(0)

	# Initialize the scanner
	s = Scanner(fileName)
	while 1:
		nextToken = s.getToken()
		if nextToken == -1:
			print "Token error"
		elif nextToken == "EOF":
			print "End of file..."
			break
		else:
			print nextToken

if __name__ == "__main__":
	main()
