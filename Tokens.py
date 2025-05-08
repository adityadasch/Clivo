from Memory import Table

class Token:
    def __init__(self, type_, value = None, collection = ''):
        self.type = type_
        self.value = value
        self.collection = collection
    def __repr__(self):
        return f'{self.type}: {self.value}' if self.value is not None else f'{self.type}'

KEYWORDS = ['void', 'func', 'scope', 'reset', 'if', 'then', 'show']
DTYPES = ['int', 'float', 'string']

DTYPE = 'DTYPE'
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
GREATER = 'GRE'
LESSER = 'LES'
COMPARITIVES = (
DEQUAL,
GEQUAL,
LEQUAL,
NEQUAL,
GREATER,
LESSER
)
COMPARITIVES_DICT = {
    DEQUAL: "==",
    GEQUAL: ">=",
    LEQUAL: "<=",
    NEQUAL: "!=",
    GREATER: ">",
    LESSER: "<"
}


REASSIGN = 'REASSIGN'
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

def get_default_for_type(dtype: str):
    match dtype:
        case 'string':
            return '\'\''
        case 'float':
            return 0.0
        case 'int':
            return 0
    return None


# noinspection PyShadowingNames
def is_compatible(self: Token, other: Token):
    d1 = '0'
    d2 = '1'

    if self.type == IDENTIFIER:
            d1 = Table.variable_table.get(self.value).dtype

    if other.type == IDENTIFIER:
        d2 = Table.variable_table.get(other.value).dtype
    else:
        d1 = self.type
        d2 = other.type

    check = (d1 == d2) or \
        (d1 == 'int' and d2 == 'float') or \
        (d1 == 'float' and d2 == 'int') or \
        (d1 == INTEGER and d2 == FLOAT) or \
        (d1 == FLOAT and d2 == INTEGER)

    return check