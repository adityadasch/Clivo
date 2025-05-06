from Lexer import Lexer, Error
from Parser import Parser

for _ in range(10):
    code = input('Code:')
    tokens = Lexer.generate_tokens(code)

    if not isinstance(tokens,list):
        print(tokens)
    print(tokens)
    Parser.parse(tokens, code)