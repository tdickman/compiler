from token import *
from constants import *

class Scanner:
	def __init__(self, fileName):
		self.fileName = fileName
		self.curLine = 1
		self.fileO = open(fileName, 'r')
		self.lookupTable = {}
		self.__seedTable()
	
	def __getChar(self):
		self.lastPos = self.fileO.tell()
		nextChar = self.fileO.read(1)
		if (nextChar == '\n'):
			self.curLine = self.curLine + 1
		return nextChar

	def __returnChar(self):
		'''Returns a character to the file buffer, so the next __getChar
		function call returns the previous letter'''
		self.fileO.seek(self.lastPos)

	def __seedTable(self):
		'''Seeds the dictionary'''
		for word in c.reserved_words:
			self.lookupTable[word] = Token(word, c.RESERVED)
		for identifier in c.operators:
			self.lookupTable[identifier] = Token(word, c.OPERATOR)
	
	def __reportError(self, message):
		'''Prints out the given error message'''
		print "Line:", self.curLine, "-", message

	def __reportWarning(self, message):
		print "Warning: " + message

	def getToken(self):
		'''Returns the next token'''
		# Begin doing stuff #
		tokenTxt = ""
		nextChar = self.__getChar()
		while 1:
			# Identifier / Reserved Word
			if nextChar in c.letter:
				while (nextChar in c.letter) or (nextChar in c.number) or (nextChar == "_"):
					tokenTxt += nextChar
					nextChar = self.__getChar()
				self.__returnChar()
				# Add to lookup table
				if tokenTxt not in self.lookupTable:
					token = Token(tokenTxt, c.IDENTIFIER)
					self.lookupTable[tokenTxt] = token
				else:
					token = self.lookupTable[tokenTxt]
				return token
			elif nextChar == "\"":
				tokenTxt += nextChar
				nextChar = self.__getChar()
				while (nextChar in c.letter) or (nextChar in c.number) or (nextChar in " _,;:.']"):
					tokenTxt += nextChar
					nextChar = self.__getChar()
				if nextChar != "\"":
					self.__reportError("Improper termination of string.")
					self.__returnChar()
					return -1 # Change this...
				else:
					tokenTxt += nextChar
				if tokenTxt not in self.lookupTable:
					token = Token(tokenTxt, c.STRING)
					self.lookupTable[tokenTxt] = token
				else:
					token = self.lookupTable[tokenTxt]
				return token
			elif nextChar in c.number:
				while (nextChar in c.number) or (nextChar == "_"):
					tokenTxt += nextChar
					nextChar = self.__getChar()
				if (nextChar == "."):
					tokenTxt += nextChar
					nextChar = self.__getChar()
				while (nextChar in c.number) or (nextChar == "_"):
					tokenTxt += nextChar
					nextChar = self.__getChar()
				self.__returnChar()
				# Add to lookup table
				if tokenTxt not in self.lookupTable:
					token = Token(tokenTxt, c.NUMBER)
					self.lookupTable[tokenTxt] = token
				else:
					token = self.lookupTable[tokenTxt]
				return token
			elif (nextChar in c.operators) or (nextChar == "!"):
				tokenTxt += nextChar
				tokenTxt += self.__getChar()
				# Check if 2 characters match
				if tokenTxt not in c.operators:
					tokenTxt = tokenTxt[:-1]
					self.__returnChar()
					if tokenTxt == "!":
						# FAILURE<<<>>><<<>>><<<>>>
						return -1
				token = self.lookupTable[tokenTxt]
				return token
			elif nextChar == "\n":
				print " --- Newline! --- "
				nextChar = self.__getChar()
			else:
				print "Unidentified character detected: '" + nextChar + "'"
				nextChar = self.__getChar()






