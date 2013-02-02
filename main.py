import sys

def main():
	# Get the filename from the command line parameters
	if (len(sys.argv) > 1):
		fileName = sys.argv[1]
	else:
		print "Usage: python main.py infile.c"
		sys.exit(0)

	# Initialize the scanner
	s = Scanner(fileName)

if __name__ == "__main__":
	main()
