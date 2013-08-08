from scanner import *
import traceback, sys

class SymbolTable:
	def __init__(self, errorReporter):
		self.reportError = errorReporter
		self.table = []
		self.gTable = []

	def push(self):
		'''Adds an level to the symbol table'''
		self.table.append([])

	def pop(self):
		'''Removes a level from the symbol table, and removes all entries from the current level'''
		self.table.pop()

	def addItem(self, token, aType, aGlobal, val=False):
		'''Adds the given token to the symbol table at the 
		current level, and sets the type to the given type.
		var=True for a variable name, False for a variable
		value. Direction should be set to false for
		everything except function parameters.'''
		if aGlobal:
			scope = self.gTable
		else:
			scope = self.table[-1]
		# Make sure variable does not already exist in the current scope
		for item in scope:
			if item['text'] == token['text']:
				self.reportError("Token error, '" + token['text']  + "' already declared in this scope")
				return False
		token['type'] = aType.upper()
		token['val'] = val
		scope.append(token)
		print token['text'] + " added to symbol table"
		self.printScope()
		return True

	def setDirection(self, direction):
		'''Sets the direction of the perviously inserted
		variable. Used for procedure parameters.'''
		self.table[-1][-1]['direction'] = direction

	def addProcedure(self, procToken):
		'''Procedures are a special case - added up one
		layer so they are properly accessible. Parameters
		are also added to them too.'''
		print "Add procedure called!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		procToken['parameters'] = self.table[-1]
		procToken['type'] = 'PROCEDURE'
		self.table[-2].append(procToken)
		print self.table

	def checkProcedure(self, procedureToken, arguments):
		'''Checks whether or not the given procedure
		call is in scope, and the arguments are correct.'''
		print "checkProcedure called"
		# Check if procedure is in scope
		print self.table
		if not self.getToken(procedureToken):
			self.reportError("Undeclared procedure called")
		# Check if arguments are correct
		print self.getToken(procedureToken)
	
	def getToken(self, token):
		for item in self.gTable:
			if item['text'] == token['text']:
				return item
		if len(self.table):
			for row in self.table:
				for item in row:
					if item['text'] == token['text']:
						return item
		return False

	def getType(self, token):
		'''Returns type of the given token'''
		# Check current scope and global scope only
		if token['type'] != 'IDENTIFIER':
			return token['type']
		for item in self.gTable:
			if item['text'] == token['text']:
				return item['type']
		if len(self.table):
			for row in self.table:
				for item in row:
					if item['text'] == token['text']:
						return item['type']
		return False
		#return token['type'] # Change this back - return type if not in table

	def checkType(self, token, expectedType):
		'''Checks to make sure the given token is of the expected type'''
		#tType = self.getType(token)
		tType = token['type']
		if not tType:
			self.reportError("Undeclared variable, " + token['text'])
			while True: pass
			return False
		if self.getType(token) != expectedType:
			self.reportError("Type error, expected '" + expectedType + "' for " + token['text'])
			return False
		return True

	def printScope(self):
		'''Prints all tokens in the current scope. Used
		for debugging'''
		print "-------------------- Scope -----------------"
		print self.table[-1]
		print "Global:"
		print self.gTable

class Parser:
	def __init__(self, fileName):
		self.errorCount = 0
		self.s = Scanner(fileName)
		self.tree = []
		self.nToken = []
		self.resync = False
		self.stepToken()
		self.symTable = SymbolTable(self.reportError)
		self.expressionType = False   # Stores type of expression for type comparison

	#def getNToken(self):
	#	self.nToken = self.s.getToken()
	#	print self.nToken
	#	return self.nToken

	def getnToken(self):
		'''Returns nToken. used instead of nToken to allow for resyncing'''
		if self.resync:
			return {'text':'','type':''}
		else:
			return self.nToken

	def stepToSemicolon(self):
		print "Stepping to semicolon"
		while self.nToken['text'] != ";":
			self.nToken = self.s.getToken()
			print self.nToken

	def stepToken(self):
		if self.resync:
			print "Resyncing. Not stepping"
		else:
			self.nToken = self.s.getToken()
			print self.getnToken()


	def parse(self):
		self.program()

	def program(self):
		self.program_header()
		self.program_body()
		print "Parsing complete.", self.errorCount, "error(s)."

	def program_header(self):
		print "\nEntering program_header\n"
		self.expectText("program", "\"program\" expected")
		if not self.identifier():
			self.reportError("Identifier expected after program")
		self.expectText("is", "\"is\" expected")

	def program_body(self):
		self.symTable.push()
		print "\nEntering program_body\n"
		# Check for declaration (can be 0-n)
		while self.getnToken()['text'] != "begin":
			self.declaration(True)
			self.expectText(";", "Semicolon expected after declaration")
		self.stepToken()
		#while self.getnToken()['text'] != "end":
		#	if self.statement():
		#		self.expectText(";", "Semicolon expected after statement")
		#	else:
		#		self.reportError("Statement expected between begin and end")
		while self.statement():
			self.expectText(";", "Semicolon expected after statement")
		print "CHECKING FOR END"
		self.expectText("end", "\"end\" expected after statements")
		#self.stepToken()
		self.expectText("program", "\"program\" expected after end")
		self.symTable.pop()
		return True

	def declaration(self, cbGlobal):
		print "\nEntering declaration\n"
		'''cbGlobal defines whether or not the declaration can be global or not.'''
		isGlobal = False
		if self.getnToken()['text'] == "global":
			if cbGlobal:
				self.stepToken()
				isGlobal = True
			else:
				self.reportError("Global declaration in non-global part")
		if not (self.procedure_declaration(isGlobal) or self.variable_declaration(isGlobal)):
			self.reportError("Expected procedure or variable declaration")
			return False
		return True

	def procedure_declaration(self, isGlobal):
		self.symTable.push()
		headerResult = self.procedure_header(isGlobal)
		if headerResult:
			self.symTable.addProcedure(headerResult)
			bodyResult = self.procedure_body()
		self.symTable.pop()
		return headerResult and bodyResult

	def procedure_header(self, isGlobal):
		print "Entering procedure_header"
		if self.getnToken()['text'] == "procedure":
			self.stepToken()
			token = self.identifier()
			if token:
				#self.symTable.addItem(token, 'PROCEDURE', isGlobal)
				self.expectText("(", "Incomplete procedure. Expected '('")
				self.parameter_list()
				self.expectText(")", "Incomplete procedure. Expected ')'")
				return token
			else:
				self.reportError("Incomplete procedure")
		return False

	def procedure_body(self):
		# Check for declaration (can be 0-n)
		while self.getnToken()['text'] != "begin":
			self.declaration(False)
			self.expectText(";", "Semicolon expected after declaration")
		self.stepToken()
		while self.getnToken()['text'] != "end":
			self.statement()
			self.expectText(";", "Semicolon expected after statement")
		self.stepToken()
		self.expectText("procedure", "\"procedure\" expected after end")
		return True

	def parameter_list(self):
		print "Entering parameter_list"
		if self.parameter():
			if self.getnToken()['text'] == ",":
				self.stepToken()
				self.parameter_list()
			return True
		else:
			self.reportError("At least one parameter expected in parameter list")
		return False

	def parameter(self):
		if self.variable_declaration():
			direction = self.getnToken()['text']
			if direction in {"in", "out"}:
				self.symTable.setDirection(direction)
				self.stepToken()
				return True
			else:
				self.reportError("'in' or 'out' expected after variable declaration in parameter")
		return False

	def type_mark(self):
		print "\nEntering type_mark\n"
		token = self.getnToken()
		if token['text'] in {"integer", "float", "bool", "string"}:
			self.stepToken()
			return token['text'].upper()
		else:
			return False

	def variable_declaration(self, isGlobal=False):
		print "\nEntering variable_declaration\n"
		aType = self.type_mark()
		if aType:
			aIdentifier = self.identifier()
			if aIdentifier:
				self.symTable.addItem(aIdentifier, aType, isGlobal)
				if self.getnToken()['text'] == "[":
					self.stepToken()
					lType = self.array_size()
					if lType == 'INTEGER':
						self.expectText("]", "Expected ']' at end of array declaration")
						return True
					else:
						self.reportError("No integer array size found")
				else:
					return True
			else:
				self.reportError("No identifier after type in variable declaration")
		return False

	def array_size(self):
		return self.number()

	def number(self):
		lType = self.getnToken()['type']
		if lType in {'INTEGER', 'FLOAT'}:
			self.stepToken()
			return lType
		else:
			return False

	def statement(self):
		'''sbGlobal defines whether or not the statement should be global or not.'''
		return ( self.if_statement() or self.loop_statement() or self.return_statement() or self.ruleInt() )
	
	def assignment_statement1(self):
		print "Entering assignment_statement"
		if self.getnToken()['text'] == "[":
			self.stepToken()
			if self.expression():
				self.expectText("]", "No ']' found after ']' in assignment statement")
				self.expectText(":=", "No ':=' found in assignment statement")
				lType = self.expression()
				if lType:
					return lType
				else:
					self.reportError("Expected expression after '=' in assignment statement")
			else:
				self.reportError("Expected ']' after expression in assignment statement")
		elif self.getnToken()['text'] == ":=":
			self.stepToken()
			lType = self.expression()
			print "assignment_statement1 =", lType
			if lType:
				return lType
			else:
				self.reportError("Expected expression after '=' in assignment statement")
		return False

	def expression(self):
		self.expressionType = False
		if self.getnToken()['text'] == "not":
			self.stepToken()
			lType = self.arithOp()
			if lType:
				rType = self.expression1()
				if rType:
					# Integers only
					if not (lType and rType in {'INTEGER', 'BOOL'}):
						self.reportError("Non-integer/bool used in expression")
					if not (lType == rType):
						self.reportError("Non-matching expression")
					return self.compatTypes(lType, rType)
				else:
					return lType
			else:
				self.reportError("unterminated 'not' in expression")
		else:
			lType = self.arithOp()
			if lType:
				rType = self.expression1()
				if rType:
					return self.compatTypes(lType, rType)
				else:
					print "Expression =", lType
					return lType
		return False

	def expression1(self):
		if self.getnToken()['text'] in {"&", "|"}:
			self.stepToken()
			lType = self.arithOp()
			if lType:
				rType = self.expression1()
				if rType:
					return self.compatTypes(lType, rType)
				else:
					return lType
			else:
				self.reportError("Invalid expression")
		return False

	def factor(self):
		nToken = self.getnToken()
		if (nToken['text'] == "true") or (nToken['text'] == "false"):
			self.stepToken()
			return 'BOOL'
		elif nToken['text'] == "(":
			self.stepToken()
			expr = self.expression()
			if expr:
				self.expectText(")", "')' expected after expression in factor")
				return expr
			else:
				self.reportError("Expression expected after '(' in factor")
		elif nToken['text'] == "-":
			self.stepToken()
			nameOrNum = self.name() or self.number()
			if nameOrNum:
				return nameOrNum
			else:
				self.reportError("- with no name of number following")
		return self.name() or self.number() or self.string()

	def name(self):
		token = self.identifier()
		if token:
			lType = token['type']
			if self.getnToken()['text'] == "[":
				self.stepToken()
				if self.expression():
					self.expectText("]", "']' expected after expression in name")
					return lType
				else:
					self.reportError("Expression expected after '[' in name")
			else:
				return lType
		return False

	def term(self):
		print "Entering term"
		lType = self.factor()
		if lType:
			rType = self.term1()
			if rType:
				if not (lType and rType in {'INTEGER', 'FLOAT'}):
					self.reportError("Non-integer/float used in arithmetic operation")
				return self.compatTypes(lType, rType, 'ARITH')
			else:
				return lType
		return False

	def term1(self):
		if self.getnToken()['text'] in {"*", "/"}:
			self.stepToken()
			lType = self.factor()
			if lType:
				rType = self.term1()
				if rType:
					if not (lType and rType in {'INTEGER', 'FLOAT'}):
						self.reportError("Non-integer/float used in arithmetic operation")
					return self.compatTypes(lType, rType, 'ARITH')
				else:
					return lType
			else:
				self.reportError("Invalid relational operation")
		return False

	def relation(self):
		lType = self.term()
		if lType:
			rType = self.relation1()
			if rType:
				return self.compatTypes(lType, rType, 'RELATION')
			else:
				return lType
		return False

	def relation1(self):
		if self.getnToken()['text'] in {"<", ">=", "<=", ">", "==", "!="}:
			self.stepToken()
			lType = self.term()
			if lType:
				rType = self.relation1()
				if rType:
					return self.compatTypes(lType, rType)
				else:
					return lType
			else:
				self.reportError("Invalid relational operation")
		return False

	def arithOp(self):
		lType = self.relation()
		if lType:
			rType = self.arithOp1()
			if rType:
				if not (lType and rType in {'INTEGER', 'FLOAT'}):
					self.reportError("Non-integer/float used in arithmetic operation")
				return self.compatTypes(lType, rType, 'ARITH')
			else:
				return lType
		return False

	def arithOp1(self):
		if self.getnToken()['text'] in {"+", "-"}:
			self.stepToken()
			lType = self.relation()
			if lType:
				rType = self.arithOp1()
				if rType:
					if not (lType and rType in {'INTEGER', 'FLOAT'}):
						self.reportError("Non-integer/float used in arithmetic operation")
					return self.compatTypes(lType, rType, 'ARITH')
				else:
					return lType
			else:
				self.reportError("Invalid arithmetic operation")
		return False

	def expCheckType(self, token):
		if self.expressionType == False:
			self.expressionType = self.symTable.getType(token)
		print "Checking if " + str(token) + " is of type " + str(self.expressionType)
		self.symTable.checkType(token, self.expressionType)

	def if_statement(self):
		print "Entering if_statement"
		if self.getnToken()['text'] == "if":
			self.stepToken()
			self.expectText("(", "'(' expected after if in if statement")
			lType = self.expression()
			if lType:
				if lType != 'BOOL':
					self.reportError("Non boolean value used in if statement")
					return False
				self.expectText(")", "')' expected in if statement")
				if self.getnToken()['text'] == "then":
					self.stepToken()
					while self.statement():
						self.expectText(";", "Semi-colon expected after statement in if statement")
					if self.getnToken()['text'] == "else":
						self.stepToken()
						while self.statement():
							self.expectText(";", "Semi-colon expected after statement in if statement")
					print "Looking for end in if statement"
					self.expectText("end", "'end' expected in if statement")
					self.expectText("if", "'if' expected after end in if statement")
					return True
					print "Completing if statement"
				else:
					self.reportError("'then' expected after expression in if statement")
			else:
				self.reportError("Expression expected after 'if'")
		return False

	def loop_statement(self):
		if self.getnToken()['text'] == "for":
			self.stepToken()
			self.expectText("(", "'(' expected after for")
			token = self.identifier()
			if token:
				lType = token['type']
			rType = self.assignment_statement1()
			print lType,rType
			if lType == rType == 'INTEGER':
				self.expectText(";", "semi-colon expected after assignment statement in for loop")
				if self.expression():
					self.expectText(")", "')' expected at end of for loop statement")
					while self.statement():
						self.expectText(";", "Semi-colon expected after statement in for loop")
					self.expectText("end", "'end' expected to close for loop")
					self.expectText("for", "'for' expected after end at end of for loop")
					return True
				else:
					self.reportError("expression expected after semi-colon in for loop")
			else:
				self.reportError("Non integer loop")
		return False

	def return_statement(self):
		if self.getnToken()['text'] == "return":
			self.stepToken()
			return True

	def procedure_call1(self):
		if self.getnToken()['text'] == "(":
			self.stepToken()
			if self.getnToken()['text'] == ")":
				self.stepToken()
				return True
			else:
				arguments = self.argument_list()
				if arguments:
					self.expectText(")", "Can't find ')' for procedure call")
					return arguments
				else:
					self.reportError("Please enter argument list or ')' to close procedure call")
		return False

	def argument_list(self):
		lType = self.expression()
		if lType:
			rType = self.argument_list1()
			if rType:
				print [lType] + rType
				return [lType] + rType
			else:
				return [lType]
		return False

	def argument_list1(self):
		if self.getnToken()['text'] == ",":
			self.stepToken()
			lType = self.expression()
			if lType:
				rType = self.argument_list1()
				if rType:
					return [lType] + rType
				else:
					return [lType]
			else:
				self.reportError("Incomplete argument list")
		return False

	def ruleInt(self):
		token = self.identifier()
		if token:
			lType = token['type']
			arguments = self.procedure_call1()
			if arguments:
				self.symTable.checkProcedure(token, arguments)
				self.symTable.checkType(token, 'PROCEDURE')
				return True
			else:
				rType = self.assignment_statement1()
				if rType:
					print "Checking assignment types"
					return self.compatTypes(lType, rType)
				else:
					self.reportError("Assignment statement or procedure call with unknown character after identifier")
		return False

	def checkAndProcede(self, text):
		'''Checks if the next token text matches the given text, and proceeds if it does'''
		if self.getnToken() == text:
			self.stepToken()
			return True
		else:
			return False
	
	def string(self):
		if self.getnToken()['type'] == 'STRING':
			self.stepToken()
			return 'STRING'
		else:
			return False

	def expectText(self, text, errorTxt):
		'''Checks for the specified text, otherwise throws an error, and returns 0'''
		if self.resync and text == ";":
			self.stepToSemicolon()
			print self.nToken
			self.resync = False
			print "Completing sync to ;"
		if self.getnToken()['text'] != text:
			if text == ";":
				self.stepToSemicolon()
				print self.nToken
			else:
				self.stepToken()
			# Throw Error
			self.reportError(errorTxt)
			return False
		else:
			self.stepToken()
			return True

	def identifier(self):
		token = self.getnToken()
		if token['type'] == 'IDENTIFIER':
			self.stepToken()
			lType = self.symTable.getType(token) 
			if lType:
				return {'text':token['text'], 'type':lType}
			return token
		else:
			return False

	def reportError(self, errorTxt):
		if self.resync:
			# Ignore error
			print "Resyncing: Ignoring errors"
		else:
			self.errorCount += 1
			self.resync = True
			self.s.reportError(errorTxt)
			#for line in traceback.format_stack():
			#	print line.strip()
		#exit()
	
	def compatTypes(self, lType, rType, caller=None):
		'''Returns whether or not the two passed in types
		are compatible with each other.'''
		if caller == 'RELATION':
			if lType and rType in {'BOOL', 'INTEGER'}:
				return 'BOOL'
		elif lType == rType:
			print lType, "==", rType
			combinedType = lType
			return combinedType
		elif caller == 'ARITH':
			if lType and rType in {'INTEGER', 'FLOAT'}:
				return 'INTEGER'
		else:
			traceback.print_stack()
			print lType, "!=", rType
			self.reportError("Incompatible types.")
			return False
