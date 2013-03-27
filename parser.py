from scanner import *
import traceback, sys

class Stack:
	'''Used to store the current state'''
	def __init__(self):
		self.stack = []

	def peek(self):
		return self.stack[-1]

	def topState(self):
		return self.stack[-1][0]

	def topItem(self):
		return self.stack[-1][1]

	def pop(self):
		return self.stack.pop()

	def push(self, state):
		self.stack.append( [state, 1] )

	def incItem(self):
		self.stack[-1][1] = self.stack[-1][1] + 1
		
	def setItem(self, value):
		self.stack[-1][1] = value
	
	def dumpStack(self):
		'''Prints out the stack for debugging purposes'''
		print self.stack

	def notEmpty(self):
		if not self.stack:
			return False
		else:
			return True

class Parser:
	def __init__(self, fileName):
		self.s = Scanner(fileName)
		self.stack = Stack()
		self.stack.push("program")
		self.tree = []
		self.nToken = []
		self.itNToken()

	def itNToken(self):
		'''Gets the next token, stores it in nToken, and returns it'''
		self.nToken = self.s.getToken()
		print "New token: " + str(self.nToken)
		return self.nToken

	def parse(self):
		syntax = {"program" : self.program,
				"program_header" : self.program_header,
				"program_body"   : self.program_body,
				"identifier"     : self.identifier
				}
		while self.stack.notEmpty():
			# Get current state, and decide what to do based on that
			topState = self.stack.topState()
			print topState
			syntax[topState]()
			# Print some stuff for debugging purposes
			print self.nToken
			self.stack.dumpStack()
			print " - - "

	def program(self):
		topItem = self.stack.topItem()
		if topItem == 1:
			self.stack.incItem()
			self.stack.push("program_header")
		elif topItem == 2:
			self.stack.incItem()
			self.stack.push("program_body")
		else:
			self.stack.pop()
			print "Completed program"

	def program_header(self):
		topItem = self.stack.topItem()
		if topItem == 1:
			self.checkTerm("program")
		elif topItem == 2:
			self.stack.incItem()
			self.stack.push("identifier")
		elif topItem == 3:
			self.checkTerm("is")
		else:
			self.stack.pop()
			print "Completed program_header"

	def program_body(self):
		topItem = self.stack.topItem()
		if topItem == 1:
			if self.nToken[1] == "begin":
				self.stack.setItem(4)
			else:
				self.stack.incItem()
				self.stack.push("declaration")
		elif topItem == 2:
			self.checkTerm(";")
		elif topItem == 3:
			if self.nToken[0] == "begin":
				self.stack.incItem()
			elif self.nToken[0] == "end":
				self.stack.setItem(7)
			else:
				self.stack.setItem(1)
		elif topItem == 4:
			if self.nToken[1] == "end":
				self.stack.setItem(7)
			else:
				self.stack.incItem()
				self.stack.push("statement")
		elif topItem == 5:
			self.checkTerm(";")
		elif topItem == 6:
			if self.nToken[0] == "end":
				self.stack.incItem()
			else:
				self.stack.setItem(4)
		elif topItem == 7:
			self.checkTerm("program")
		else:
			self.stack.pop()
			print "Completed program body"

	def declaration(self):
		print "Nothing here yet..."

	def identifier(self):
		if self.nToken[1] == 'IDENTIFIER':
			self.stack.pop()
			print "Identifier: " + self.nToken[0]
			self.itNToken()
		else:
			print "Error... Exiting" # Throw a real error...
			traceback.print_exc(file=sys.stdout)
			exit()

	def checkTerm(self, term):
		'''Compares the given token to make sure it is the proper
		termination. Otherwise it throws an error!'''
		if self.nToken[0] != term:
			print "Error... Exiting" # Throw a real error...
			traceback.print_exc(file=sys.stdout)
			exit()
		else:
			self.stack.incItem()
			self.itNToken()
