from Lexer import Lexer
from Parser import Parser

with open('source/example.clivo', 'r') as f:
    line = f.read()
for _code in line.split('\n'):
    tokens = Lexer.generate_tokens(_code)
    if len(tokens) > 0:
        Parser.parse(tokens, _code)