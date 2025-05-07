import Tokens

class Variable:
    def __init__(self, value, dtype):
        self.value = value
        self.dtype = dtype

    def __repr__(self):
        return f'{self.value} ({self.dtype})'

class Scope:
    def __init__(self):
        self.execution_tree = None
        self.variables: dict = dict()
        self.scopes: dict = dict()
        self.arguments: dict[str, Variable] = dict()

class ClassScope(Scope):
    def __init__(self):
        super().__init__()
        self.methods: dict = dict()

class FunctionScope(Scope):
    def __init__(self):
        super().__init__()

class Table:
    variable_table: dict = dict() # Identifier: Index in value_table
    scope_table: dict[str, Scope] = dict() # Scope Id: Scope Object
    function_table: dict = dict() # Identifier: Function Scope Object
    class_table: dict = dict() # Identifier: Class Scope Object
    callable_table: dict = dict() #

    @classmethod
    def create_variable(cls, name, value, dtype):
        cls.variable_table[name] = Variable(value, dtype)

    @classmethod
    def update_variable(cls, name, value):
        cls.variable_table.get(name).value = value
