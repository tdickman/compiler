from scanner import *

class Stack:
	'''Used to store the current state'''
	def __init__(self):
		self.stack = []

	def peek(self):
		return self.stack[-1]

	def curState(self):
		return self.stack[-1][0]

	def curItem(self):
		return self.stack[-1][1]

	def pop(self):
		return self.stack.pop()

	def push(self, state):
		self.stack.append( (state, 1) )

	def incItem(self):
		self.stack[-1][1] += 1
		
	def setItem(self, value):
		self.stack[-1][1] = value

class Parser:
	def __init__(self, fileName):
		self.s = Scanner(fileName)
		self.stack = Stack()
		self.stack.push("program")
		self.tree = []
		self.syntax = {"program" : program,
				"program_header" : program_header
				"identifier"     : identifier
				}

	def parse(self):
		while 1:
			nToken = self.s.getToken()
			# Get current state, and decide what to do based on that
			curItem = self.stack.curItem()
			self.syntax[curItem](nToken)


			if nToken == "program":
				self.stack.append()
			if nextToken == -1:
				print "Token error"
			elif nextToken == "EOF":
				print "End of file..."
				break
			else:
				print nextToken

	def program(self, nToken):
		curItem = self.stack.curItem()
		if curItem == 1:
			self.stack.incItem()
			self.stack.push("program_header")
		elif curItem == 2:
			self.stack.incItem()
			self.stack.push("program_body")
		else:
			self.stack.pop()
			print "Completed program"

	def program_header(self, nToken):
		curItem = self.stack.curItem()
		if curItem == 1:
			self.checkTerm(nToken, "program")
		elif curItem == 2:
			self.stack.incItem()
			self.stack.push("identifier")
		elif curItem == 3:
			self.checkTerm(nToken, "is")
		else:
			self.stack.pop()
			print "Completed program_header"

	def program_body(self, nToken):
		curItem = self.stack.curItem()
		if curItem == 1:
			self.stack.push("declaration")
		elif curItem == 2:
			self.checkTerm(nToken, ";")
		elif curItem == 3:
			if nToken[1] == "begin":
				self.stack.incItem()
			else:
				self.stack.setItem(1)
		elif curItem == 4:
			self.stack.push("declaration")
		elif curItem == 5:
			self.checkTerm(nToken, ";")
		elif curItem == 6:
			self.checkTerm(nToken, "end")
		elif curItem == 7:
			self.checkTerm(nToken, "program")
		else:
			self.stack.pop()
			print "Completed program body"

	def declaration(self, nToken):


	def checkTerm(self, token, term):
		'''Compares the given token to make sure it is the proper
		termination. Otherwise it throws an error!'''
		if token[0] != term:
			print "Error" # Throw a real error...
		else:
			self.stack.incItem()
