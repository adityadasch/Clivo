from Tokens import *
from nodes import *

class TokenStream:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    @property
    def peek(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def advance(self):
        self.position += 1 if self.position < len(self.tokens) else None

class Parser:
    ast: list

    @classmethod
    def parse_tree(cls):
        for index, node in enumerate(cls.ast):
            node.execute()

Parser.ast = [IfNode(
    BoolCompNode(BinOpNode(BinOpNode(2,'+',3),'*',5), '==', 25),
    ShowNode('True'),
    [ShowNode('Not true'), ShowNode('Multi line working')]

)]
Parser.parse_tree()