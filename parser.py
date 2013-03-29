from scanner import *
import traceback, sys

class Parser:
	def __init__(self, fileName):
		self.s = Scanner(fileName)
		self.tree = []
		self.nToken = []
		self.getNToken()

	def getNToken(self):
		self.nToken = self.s.getToken()
		print self.nToken
		return self.nToken

	def stepToken(self):
		self.nToken = self.s.getToken()
		print self.nToken

	def parse(self):
		self.program()

	def program(self):
		self.program_header()
		self.program_body()

	def program_header(self):
		print "\nEntering program_header\n"
		self.expectText("program", "\"program\" expected")
		self.identifier()
		self.expectText("is", "\"is\" expected")

	def program_body(self):
		print "\nEntering program_body\n"
		# Check for declaration (can be 0-n)
		while self.nToken['text'] != "begin":
			self.declaration(True)
			self.expectText(";", "Semicolon expected after declaration")
		self.stepToken()
		while self.nToken['text'] != "end":
			if not self.statement():
				self.reportError("Statement expected between begin and end")
			self.expectText(";", "Semicolon expected after statement")
		self.stepToken()
		self.expectText("program", "\"program\" expected after end")
		return True

	def declaration(self, sbGlobal):
		print "\nEntering declaration\n"
		'''sbGlobal defines whether or not the declaration should be global or not.'''
		if sbGlobal:
			self.expectText("global", "Non-global declaration in global section")
		if not (self.variable_declaration() or self.procedure_declaration()):
			self.reportError("Expected procedure or variable declaration")
			return False
		return True

	def procedure_declaration(self):
		return self.procedure_header() and self.procedure_body()

	def procedure_header(self):
		if self.nToken['text'] != "procedure":
			return False
		self.stepToken()
		if self.getNToken()['type'] != 'IDENTIFIER':
			self.reportError("Expected identifier after procedure")
			return False
		if self.getNToken()['text'] != "(":
			self.reportError("Expected '(' after identifier in procedure")
			return False
		self.parameter_list()
		if self.getNToken()['text'] != ")":
			self.reportError("Expected ')' to close parameter list in procedure")
			return False

	def procedure_body(self):
		# Check for declaration (can be 0-n)
		while self.nToken['text'] != "begin":
			self.declaration(False)
			self.expectText(";", "Semicolon expected after declaration")
		self.stepToken()
		while self.nToken['text'] != "end":
			self.statement()
			self.expectText(";", "Semicolon expected after statement")
		self.stepToken()
		self.expectText("procedure", "\"procedure\" expected after end")
		return True

	def parameter_list(self):
		while self.nToken['text'] != ")":
			self.parameter()

	def parameter(self):
		if self.variable_declaration():
			self.stepToken()
		else:
			return False
		if (self.nToken['text'] == "in") or (self.nToken['text'] == "out"):
			return True
		else:
			self.reportError("'in' or 'out' not specified after variable_declaration in parameter")
			return False

	def type_mark(self):
		print "\nEntering type_mark\n"
		tText = self.getNToken()['text']
		return (tText == "integer" or "float" or "bool" or "string")

	def variable_declaration(self):
		print "\nEntering variable_declaration\n"
		if ( self.type_mark() and self.identifier() ):
			if self.nToken['text'] == "[":
				self.stepToken()
				return self.array_size() and (self.getNtoken()['text'] == "]")
			else:
				return True
		else:
			return False

	def array_size(self):
		return self.number()

	def number(self):
		return (self.getNtoken()['type'] == 'NUMBER')

	def statement(self):
		'''sbGlobal defines whether or not the statement should be global or not.'''
		return ( self.if_statement() or self.loop_statement() or self.return_statement() or self.ruleInt() )
	
	def assignment_statement1(self):
		print "Entering assignment_statement"
		if self.nToken['text'] == "[":
			self.stepToken()
			if self.expression():
				self.expectText("]", "No ']' found after ']' in assignment statement")
				self.expectText("=", "No '=' found in assignment statement")
				if self.expression():
					return True
				else:
					self.reportError("Expected expression after '=' in assignment statement")
			else:
				self.reportError("Expected ']' after expression in assignment statement")
		elif self.nToken['text'] == "=":
			self.stepToken()
			if self.expression():
				return True
			else:
				self.reportError("Expected expression after '=' in assignment statement")
		return False

	def expression(self):
		self.reportError("expression not implemented")
		if self.arithOp():
			return True
		elif self.nToken['text'] == "not":
			self.stepToken()
			if self.arithOp():
				return True
			else:
				self.reportError("Arithmetic operation expected expression")
		elif self.expression():
			if self.nToken['text'] in {"&", "|"}:
				self.stepToken()
				if self.arithOp():
					return True
				else:
					self.reportError("arithOp expected after '&' or '|' in expression")
			else:
				self.reportError("'&' or '|' expected in expression")
		return False

	def factor(self):
		if (self.nToken['text'] == "true") or (self.nToken['text'] == "false"):
			self.stepToken()
			return True
		elif self.nToken['text'] == "(":
			self.stepToken()
			if self.expression():
				self.expectText(")", "')' expected after expression in factor")
				return True
			else:
				self.reportError("Expression expected after '(' in factor")
		elif self.nToken['text'] == "-":
			if (self.name() or self.number()):
				return True
			else:
				self.reportError("- with no name of number following")
		elif (self.name() or self.number()):
			return True
		elif self.string():
			return True
		return False

	def name(self):
		if self.identifier():
			if self.nToken() == "[":
				self.stepToken()
				if self.expression():
					self.expectText("]", "']' expected after expression in name")
					return True
				else:
					self.reportError("Expression expected after '[' in name")
			else:
				return True
		return False

	def term(self):
		print "Entering term (debugging might be necessary"
		if self.factor():
			return True
		elif self.term():
			if (self.nToken['text'] == "*") or (self.nToken['text'] == "/"):
				self.stepToken()
				if self.factor():
					return True
				else:
					self.reportError("Factor expected after '*' or '/'")
			else:
				self.reportError("* or / expected after term")
		return False

	def relation(self):
		if self.term():
			return True
		elif self.relation():
			if self.nToken['text'] in {"<", ">=", "<=", ">", "==", "!="}:
				self.stepToken()
				if self.term():
					return True
				else:
					self.reportError("Term expected after comparator symbol")
			else:
				self.reportError("Comparator expected after term in relation")
		return False

	def arithOp(self):
		if self.relation():
			return True
		elif self.arithOp():
			if self.nToken['text'] in {"+", "-"}:
				self.stepToken()
				if self.relation():
					return True
				else:
					self.reportError("Relation expected after '+' or '-' symbol")
			else:
				self.reportError("'+' or '-' expected after arithOp")
		return False

	def if_statement(self):
		if self.nToken['text'] == "if":
			self.stepToken()
			if self.expression():
				if self.nToken['text'] == "then":
					self.stepToken()
					while self.statement():
						self.expectText(";", "Semi-colon expected after statement in if statement")
					if self.nToken['text'] == "else":
						self.stepToken()
						while self.statement():
							self.expectText(";", "Semi-colon expected after statement in if statement")
					self.expectText("end", "'end' expected in if statement")
					self.expectText("if", "'if' expected after end in if statement")
				else:
					self.reportError("'then' expected after expression in if statement")
			else:
				self.reportError("Expression expected after 'if'")
		return False

	def loop_statement(self):
		if self.nToken['text'] == "for":
			self.expectText("(", "'(' expected after for")
			if self.identifier() and self.assignment_statement1():
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
				self.reportError("assignment statement expected after '(' in for loop")
		return False

	def return_statement(self):
		if self.nToken['text'] == "return":
			self.stepToken()
			return True

	def procedure_call1(self):
		if self.nToken['text'] == "(":
			self.stepToken()
			if self.nToken['text'] == ")":
				self.stepToken()
				return True
			elif self.argument_list():
				self.expectText(")", "Can't find ')' for procedure call")
				return True
			else:
				self.reportError("Please enter argument list or ')' to close procedure call")
		else:
			self.reportError("Unterminated procedure call")
		return False

	def argument_list(self):
		while self.expression():
			self.expectText(",", "Comma expected after expression in argument_list")

	def ruleInt(self):
		if self.identifier():
			if self.procedure_call1():
				return True
			elif self.assignment_statement1():
				return True
			else:
				self.reportError("Assignment statement or procedure call with unknown character after identifier")
		return False

	def checkAndProcede(self, text):
		'''Checks if the next token text matches the given text, and proceeds if it does'''
		if self.nToken == text:
			self.stepToken()
			return True
		else:
			return False
	
	def string(self):
		if self.nToken['type'] == 'STRING':
			self.stepToken()
			return True
		else:
			return False

	def expectText(self, text, errorTxt):
		'''Checks for the specified text, otherwise throws an error, and returns 0'''
		if self.nToken['text'] != text:
			self.stepToken()
			# Throw Error
			self.reportError(errorTxt)
			return False
		else:
			self.stepToken()
			return True

	def identifier(self):
		if self.nToken['type'] != 'IDENTIFIER':
			return False
		else:
			self.stepToken()
			return True

	def reportError(self, errorTxt):
		self.s.reportError(errorTxt)
		for line in traceback.format_stack():
			print line.strip()
		exit()
