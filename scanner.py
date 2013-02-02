class TokenType(object):
	reserved = 0
	identifier = 1
	string = 2
	number = 3
	operator = 4

class Scanner:
	# Define types
	RESERVED = 0
	IDENTIFIER = 1
	STRING = 2
	NUMBER = 3
	OPERATOR = 4
	UNKNOWN = 5
	# Stuff to pre-seed symbol table with
	reserved_words = {"string", "int", "bool", "float", "global", \
		"in", "out", "if", "then", "else", "case", "for", \
		"and", "or", "not", "program", "procedure", "begin", \
		"return", "end"}
	identifiers = {":", ";", ",", "+", "-", "*", "/", "(", ")", \
		"<", "<=", ">", ">=", "!=", "=", ":=", "{", "}"}
	
	def __init__(self, fileName):
		self.fileName = fileName
		self.curLine = 1
		self.fileO = open(fileName)
		self.lookupTable = {}
		self.__seedTable()
	
	def __getChar(self):
		nextChar = self.fileO.read(1)
		if (nextChar == '\n'):
			self.curLine = self.curLine + 1
		return nextChar

	def __seedTable(self):
		'''Seeds the dictionary'''
		for word in reserved_words:
			self.lookupTable[word] = RESERVED
		for identifier in identfiers:
			self.lookupTable[identifier] = IDENTIFIER
	
	def __reportError(self, message):
		'''Prints out the given error message'''
		print "Error: " + message

	def __reportWarning(self, message):
		print "Warning: " + message

	def getToken(self):
		'''Returns the next token'''
		print self.__nextChar()
