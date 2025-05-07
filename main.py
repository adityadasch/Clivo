from Lexer import Lexer, Error
from Parser import Parser

for _ in range(100):
    code = input('Code:')
    tokens = Lexer.generate_tokens(code)

    if not isinstance(tokens,list):
        print(tokens)
    Parser.parse(tokens, code)