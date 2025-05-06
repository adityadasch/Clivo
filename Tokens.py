class Token:
    def __init__(self, type_, value = None):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f'{self.type}: {self.value}' if self.value is not None else f'{self.type}'

KEYWORDL = ['int', 'float', 'string', 'void']

STRING = 'STRING'
NUMBER = 'NUMBER'
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
KEYWORD = 'KEYWORD'
IDENTIFIER = 'IDENTIFIER'
ACCESS = 'ACCESS'
NEWLINE = 'NL'
TAB = 'TB'
EQUAL = 'EQ'
DEQUAL = 'DEQ'
GEQUAL = 'GEQ'
LEQUAL = 'LEQ'
PEQUAL = 'PEQ'
MEQUAL = 'MEQ'
MULEQUAL = 'MUEQ'
DIVEQUAL = 'DIEQ'
MODEQUAL = 'MOEQ'
NEQUAL = 'NEQ'
REASSIGN = 'REASSIGN'

GREATER = 'GRE'
LESSER = 'LES'
PLUS = 'ADD'
MINUS = 'MIN'
MUL = 'MUL'
CARAT = 'CAR'
DIV = 'DIV'
HASH = 'HSH'
MOD = 'MOD'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'
LEFT_PAREN = 'LPAREN'
RIGHT_PAREN = 'RPAREN'
LEFT_BRACE = 'LBRC'
RIGHT_BRACE = 'RBRC'
LEFT_SET = 'LSET'
RIGHT_SET = 'RSET'
COLON = 'COL'
SEMICOLON = 'SCL'

END = 'END'