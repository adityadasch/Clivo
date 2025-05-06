import Tokens
from Error import Error, SyntaxError
from Tokens import *

class Lexer:
    @staticmethod
    def generate_tokens(code: str):
        # code += 'Ʃ'
        # ---------------- Variables---------------------
        tokens = []
        count = 0
        code = code.replace('    ', '\t')
        basic_characters = {'\n':NEWLINE, '\t': TAB,
                            '=': EQUAL, '+': PLUS, '-': MINUS, '*': MUL, '^':'CARAT',
                            '/': DIV, '#':HASH, '%':MOD, '&':AND, '|': OR, '!': NOT,
                            '(': LEFT_PAREN, ')': RIGHT_PAREN, '[': LEFT_BRACE, ']': RIGHT_BRACE,
                            '{': LEFT_SET, '}': RIGHT_SET, ':': COLON, ';': SEMICOLON, '$':ACCESS,
                            '>': GREATER, '<': LESSER
                            }
        alpha = 'abcdefghijklmnopqrstuvwxyz' + 'abcdefghijklmnopqrstuvwxyz'.upper()
        numeric = '0123456789'
        alpha_numeric = alpha + numeric

        while count < len(code):
            if code[count] in basic_characters:
                tokens.append(Token(basic_characters.get(code[count])))

            elif code[count] == '"' or code[count] == "'":
                check = '"' if code[count] == '"' else code[count]
                string = ''
                run = True
                count += 1
                while run:
                    if count >= len(code):
                        return SyntaxError('Console','1','Missing quotation(") mark', code)
                    print(count, code[count])
                    if code[count] == check:
                        break
                    string += code[count]
                    count += 1
                tokens.append(Token(STRING,string))
                count += 1
                continue

            elif code[count] in alpha:
                string = code[count]
                count = count + 1
                while count < len(code) and code[count] in alpha_numeric :
                    string += code[count]
                    count += 1
                tokens.append(Token(KEYWORD if string in KEYWORDL else IDENTIFIER ,string))
                continue

            elif code[count] in numeric:
                string = code[count]
                count = count + 1
                while count < len(code) and (code[count] in numeric or code[count] == '.') :
                    string += code[count]
                    count += 1
                tokens.append(Token(NUMBER,string))
                continue

            count += 1

        return Lexer.compress(tokens)

    @staticmethod
    def compress(tokens:list[Token]):
        pop_tok = []
        for index, token in enumerate(tokens):
            if token.type == Tokens.EQUAL and index > 0:
                if tokens[index - 1].type == Tokens.EQUAL:
                    pop_tok.append(index)
                    tokens[index-1].type = Tokens.DEQUAL
                elif tokens[index - 1].type == Tokens.GREATER:
                    pop_tok.append(index)
                    tokens[index-1].type = Tokens.GEQUAL
                elif tokens[index - 1].type == Tokens.LESSER:
                    pop_tok.append(index)
                    tokens[index-1].type = Tokens.LEQUAL
                elif tokens[index - 1].type == Tokens.PLUS:
                    pop_tok.append(index)
                    tokens[index-1].type = Tokens.PEQUAL
                elif tokens[index - 1].type == Tokens.MINUS:
                    pop_tok.append(index)
                    tokens[index-1].type = Tokens.MEQUAL
                elif tokens[index - 1].type == Tokens.MUL:
                    pop_tok.append(index)
                    tokens[index-1].type = Tokens.MULEQUAL
                elif tokens[index - 1].type == Tokens.COLON:
                    pop_tok.append(index)
                    tokens[index-1].type = Tokens.REASSIGN
                elif tokens[index - 1].type == Tokens.MOD:
                    pop_tok.append(index)
                    tokens[index-1].type = Tokens.MODEQUAL
                elif tokens[index - 1].type == Tokens.DIV:
                    pop_tok.append(index)
                    tokens[index-1].type = Tokens.DIVEQUAL
                elif tokens[index - 1].type == Tokens.NOT:
                    pop_tok.append(index)
                    tokens[index-1].type = Tokens.NEQUAL
        for p in pop_tok:
            tokens.pop(p)
        return tokens