from constants import *

class Token:
	tText = ""
	tType = c.UNKNOWN
	def __init__(self, theText, theType):
		self.tText = theText
		self.tType = theType

	def getType(self):
		return self.tType

	def getText(self):
		return self.tText

	def getPrettyType(self):
		'''Used for debugging'''
		if self.tType == c.RESERVED:
			return "Reserved"
		elif self.tType == c.IDENTIFIER:
			return "Identifier"
		elif self.tType == c.STRING:
			return "String"
		elif self.tType == c.NUMBER:
			return "Number"
		elif self.tType == c.OPERATOR:
			return "Operator"
