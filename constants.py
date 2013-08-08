class c:
	'''Used for defining constants, so I don't have to type out self :)'''
	# Define lowercase and uppercase letters
	lowercase = "abcdefghijklmnopqrstuvwxyz"
	uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	letter = lowercase + uppercase
	number = "0123456789"
	letterOrNumber = letter + number
	
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
	operators = {":", ";", ",", "+", "-", "*", "/", "(", ")", \
		"<", "<=", ">", ">=", "!=", "==", "=", ":=", "{", "}", "[", "]", "&"}
