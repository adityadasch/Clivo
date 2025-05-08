class Variable:
    def __init__(self, value, dtype):
        self.value = value
        self.dtype = dtype

    def __repr__(self):
        return f'{self.value} ({self.dtype})'

    @property
    def dt_value(self):
        match self.dtype:
            case 'int':
                return int(self.value)
            case 'float':
                return float(self.value)
            case 'string':
                return str(self.value)
            case _:
                return  None

class Scope:
    def __init__(self):
        self.tokens = []
        self.variable_table: dict[str, Variable] = dict()
        self.scope_table: dict = dict()
        self.function_table: dict = dict()
        self.class_table: dict = dict()
        self.callable_table: dict = dict()
        self.arguments: dict[str, Variable] = dict()

    def create_variable(self, name, value, dtype):
        self.variable_table[name] = Variable(value, dtype)

    def update_variable(self, name, value):
        self.variable_table.get(name).value = value

class ClassScope(Scope):
    def __init__(self):
        super().__init__()
        self.methods: dict = dict()

class FunctionScope(Scope):
    def __init__(self):
        super().__init__()

class Table:
    variable_table: dict[str, Variable] = dict() # Identifier: Index in value_table
    scope_table: dict[str, Scope] = dict() # Scope Id: Scope Object
    function_table: dict = dict() # Identifier: Function Scope Object
    class_table: dict = dict() # Identifier: Class Scope Object
    callable_table: dict = dict() #
    last_result:bool = False

    @classmethod
    def create_variable(cls, name, value, dtype):
        cls.variable_table[name] = Variable(value, dtype)

    @classmethod
    def update_variable(cls, name, value):
        cls.variable_table.get(name).value = value

    @classmethod
    def get_variable(cls,name):
        return cls.variable_table.get(name)
