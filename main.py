from Lexer import Lexer, HASH
from Parser import Parser
from sys import argv

with open(argv[1], 'r') as f:
    code = f.read().split('\n')
line = 0
while line < len(code):
    _code = code[line]
    tokens = Lexer.generate_tokens(_code)
    if len(tokens) > 0 and tokens[0].type != HASH:
        line_ = Parser.parse(tokens, _code,argv[1],line)
        if line_ is not None:
            line = line_
    line+=1