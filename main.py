import sys
from scanner import *

def scanIt(scanner):
	nextToken = scanner.getToken()
	if nextToken == -1:
		print "Token error"
	else:
		print nextToken.getPrettyType() + ": " + nextToken.getText()
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
		scanIt(s)

if __name__ == "__main__":
	main()
