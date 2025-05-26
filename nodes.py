from Error import raise_, SyntaxError

class Node:
    def execute(self):
        pass
    def __str__(self):
        raise_(SyntaxError(None, None, None, None))

def run(nodes: list[Node]|tuple[Node]):
    for index, node in enumerate(nodes):
        node.execute()

class BinOpNode(Node):
    def __init__(self, left = None, op = None, right = None):
        self.left = left if not isinstance(left,Node) else left.execute()
        self.op = op
        self.right = right if not isinstance(right,Node) else right.execute()

    def __str__(self):
        return str(self.execute())

    def execute(self):
        match self.op:
            case '+':
                return eval(f'{self.left} + {self.right}')
            case '-':
                return eval(f'{self.left} - {self.right}')
            case '*':
                return eval(f'{self.left} * {self.right}')
            case '/':
                return eval(f'{self.left} / {self.right}')
            case '%':
                return eval(f'{self.left} % {self.right}')
            case '^':
                return eval(f'{self.left} ** {self.right}')
        return None

class ShowNode(Node):
    def __init__(self, message: str|Node):
        self.message = message

    def execute(self):
        if isinstance(self.message, str):
            print(self.message)
        if isinstance(self.message, Node):
            print(self.message)

class BoolCompNode(Node):
    def __init__(self, op1, sign, op2=None):
        self.op1 = op1 if not isinstance(op1,Node) else op1.execute()
        self.sign = sign
        if self.sign not in ['==','!=','>','<','>=','<=','&','|','$','!']:
            raise_(SyntaxError(None,None, None, None))
        self.op2 = op2 if not isinstance(op2,Node) else op2.execute() if op2 else True

    def execute(self):
        if self.sign in ['==', '!=','>','<','>=','<=']:
            return str(eval(f'{self.op1}{self.sign}{self.op2}'))
        match self.sign:
            case '&':
                return str(eval(f'{self.op1} == True and {self.op2} == True'))
            case '|':
                return str(eval(f'{self.op1} == True or {self.op2} == True'))
            case '$':
                return str(eval(f'({self.op1} == True or {self.op2} == True) and {self.op1} != {self.op2}'))
            case _:
                return str(False)
    def __str__(self):
        return self.execute()

class IfNode(Node):
    def __init__(self, condition: str|Node, body: list[Node]|Node, else_: list[Node]|Node = None):
        self.condition =  condition
        self.body = body if not isinstance(body, Node) else (body,)
        self.else_ = else_ if not isinstance(else_, Node) else (else_,)

    def execute(self):
        if self.condition.__str__() == 'True':
            run(self.body)
        elif self.else_:
            run(self.else_)