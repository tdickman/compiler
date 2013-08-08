compiler
========

Description
This compiler compiles programs that are written in the defined language provided to us. The compiler is written in python.

The compiler is composed of two main parts:
-Scanner - Takes the source code as an input, and outputs tokens to the parser one at a time.
-Parser - Retrieves tokens from the scanner, and performs scanning, parsing, syntax analysis, error reporting, and code generation.

Running
The following syntax is used to run this compiler on given source code:
python main.py input.src [-v]

When input.src is the input source file. Verbose output can be enabled using the -v option, but be forewarned, this outputs a LOT of text, and is really only useful for debugging the compiler.

Notes
Several of the rules were rewritten to allow them to work with this LL(1) recursive descent compiler.

Test Programs
Several test program are included to test this system:
test_program_broken.src - This program has several errors, including an undeclared variable, improper variable assignment, and an improper procedure call.
test_program.src - This program has correct grammar, and returns with 0 errors.
test_program_*.src - The rest of the programs in the folder test specific features of the compiler, including arithmetic operations, arrays, loops, etc.

