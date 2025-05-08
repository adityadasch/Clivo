import Tokens
from Memory import Table, ClassScope, FunctionScope, Variable, Scope
from Error import RunTimeError, SyntaxError, KeyError, raise_, DataTypeError
from Tokens import IDENTIFIER


def token_to_dtype(token):
    if token == Tokens.INTEGER:
        return 'int'
    elif token == Tokens.FLOAT:
        return 'float'
    elif token == Tokens.STRING:
        return 'str'
    else:
        return None

class Parser:
    @staticmethod
    def parse(tokens: list[Tokens.Token], code, file = 'Console', line:int = 1):
        if tokens[-1].type != Tokens.END:
            raise_(SyntaxError(file,line,"Semi-colon is missing", code, column = len(code.rstrip())))
        for index in range(len(tokens)):
            token = tokens[index]
            if Table.ignore_code:
                if token.type == Tokens.KEYWORD and token.value == 'end':
                    Table.ignore_code = False
                else:
                    return None
            if tokens[index].type == Tokens.REASSIGN:
                if tokens[index - 1].type == Tokens.IDENTIFIER and tokens[index + 1].type == Tokens.IDENTIFIER:
                    if Table.variable_table.get(tokens[index - 1].value).dtype == Table.variable_table[
                        tokens[index + 1].value].dtype:
                        Table.variable_table[tokens[index - 1].value] = Table.variable_table.get(
                            tokens[index + 1].value)
                    else:
                        raise_(RunTimeError(file, line,
                                            f'Cannot assign {Table.variable_table[tokens[index - 2].value].value} the given value. Convert the value before assigning',
                                            code))

            elif token.type == Tokens.IDENTIFIER:
                if len(tokens) > 1 and tokens[index + 1].type == Tokens.EQUAL:
                    if Table.variable_table.get(token.value) is None:
                        dtype = tokens[index - 1].value if Table.variable_table.get(token.value) is None else Table.variable_table.get(token.value).value

                        value = tokens[index + 2].value if len(tokens) == index + 4 else Parser.parse_exp(tokens[index + 2::]) # = Token ;
                        Table.create_variable(
                            token.value,
                            value,
                            dtype
                        )
                        if not Table.variable_table.get(token.value).check():
                            raise_(DataTypeError(file, line,"The given value is not of the same type", code))

                    else:
                        prev = Table.variable_table[token.value].value
                        value = tokens[index + 2].value if Table.variable_table.get(
                            tokens[index + 2].value) is None else Table.variable_table.get(tokens[index + 2].value).value
                        Table.update_variable(token.value, value)
                        if not Table.variable_table.get(token.value).check():
                            raise_(DataTypeError(file, line,"The given value is not of the same type", code))

                elif len(tokens) > 1 and tokens[index - 1].type == Tokens.DTYPE:
                    dtype = tokens[index - 1].value
                    Table.create_variable(
                        token.value,
                        Tokens.get_default_for_type(dtype),
                        dtype
                    )

                elif len(tokens) > 1 and tokens[index - 1].type == Tokens.KEYWORD:
                    pass
                elif len(tokens) > 1 and tokens[index + 1].type == Tokens.INCREMENT:
                    if Table.get_variable(token.value).dtype in ['int','float']:
                        new_value = Table.get_variable(token.value).dt_value + 1
                        Table.update_variable(token.value, new_value)

            elif token.type == Tokens.KEYWORD:
                if token.value == 'reset':
                    name = tokens[index + 1]
                    dtype = Table.variable_table.get(tokens[index + 1].value).dtype
                    Table.create_variable(
                        name.value,
                        Tokens.get_default_for_type(dtype),
                        dtype
                    )

                elif token.value == 'show':
                    to_show = tokens[index+1]
                    end = '\n'
                    try:
                        if tokens[index+2].type == Tokens.KEYWORD and tokens[index+2].value == 'end':
                            end = tokens[index+3].value
                    except IndexError:
                        pass
                    print(Table.variable_table.get(to_show.value).value if to_show.type == IDENTIFIER else to_show.value, end = end)

                elif token.value == 'if':
                    if tokens[index + 1].type == Tokens.LEFT_PAREN:
                        braces = tokens[index + 1:]
                        condition = None
                        for i, ele in enumerate(braces):
                            if ele.type == Tokens.RIGHT_PAREN:
                                condition = tokens[index + 2: i+1]
                        if condition is None:
                            raise_(SyntaxError(file,line,"Parenthesis are missing",code, column = len(code)))
                        for i, ele in enumerate(condition):
                            if ele.type in Tokens.COMPARITIVES:
                                left = condition[:i]
                                right = condition[i+1:]

                                left = Parser.parse_exp(left) if len(left) > 1 else left[0]
                                right = Parser.parse_exp(right) if len(right) > 1 else right[0]
                                if isinstance(left, Tokens.Token):
                                    if left.type == Tokens.IDENTIFIER:
                                        left_ = Table.get_variable(left.value)
                                        if left_ is None:
                                            raise_(KeyError(file,line,'Variable is not found', code, column=code.find(left.value)))
                                        else:
                                            left = left_.dt_value
                                    else:
                                        match left.type:
                                            case Tokens.INTEGER:
                                                left = int(left.value)
                                            case Tokens.FLOAT:
                                                left = float(left.value)
                                            case _:
                                                left = left.value
                                if isinstance(right, Tokens.Token):
                                    if right.type == Tokens.IDENTIFIER:
                                        right_ = Table.get_variable(right.value)
                                        if right_ is None:
                                            raise_(KeyError(file,line,'Variable is not found', code, column=code.find(right.value)))
                                        else:
                                            right = right_.dt_value
                                    else:
                                        match right.type:
                                            case Tokens.INTEGER:
                                                right = int(right.value)
                                            case Tokens.FLOAT:
                                                right = float(right.value)
                                            case _:
                                                right = right.value
                                res = eval(
                                    str(left) + Tokens.COMPARITIVES_DICT.get(ele.type) + str(right)
                                )
                        Table.last_result = res

                elif token.value == 'then':
                    if Table.last_result:
                        return Parser.parse(tokens[1::], code, file, line)
                    else:
                        break

                elif token.value == 'label':
                    name = tokens[index+1].value
                    Table.labels[name] = line
                    Table.ignore_code = True

                elif token.value == 'goto':
                    try:
                        name = tokens[index+1].value
                        return Table.labels[name]
                    except IndexError:
                        continue

                elif token.value == 'del':
                    if tokens[index+1].type == Tokens.VARIABLE:
                        try:
                            name = tokens[index+2]
                            del Table.variable_table[name.value]
                        except IndexError:
                            raise_(KeyError(file,line,"Variable not found", 1))
                    if tokens[index+1].type == Tokens.LABEL:
                        try:
                            name = tokens[index+2]
                            del Table.labels[name.value]
                        except IndexError:
                            raise_(KeyError(file,line,"Label not found", 1))

                elif token.value == 'cast':
                    try:
                        variable = tokens[index + 1]
                        dtype = tokens[index + 3]

                        var = Table.variable_table.get(variable.value)
                        if var is None:
                            raise_(KeyError(file, line, 'Variable not found', code, column= code.find(variable.value)))
                        var.dtype = dtype.value
                        match dtype.value:
                            case 'str':
                                var.value = str(var.value)
                            case 'int':
                                var.value = int(var.value)
                            case 'float':
                                var.value = float(var.value)
                    except IndexError:
                        raise_(SyntaxError(file, line, "Not enough arguments provided", code))
                    except ValueError:
                        raise_(DataTypeError(file,line,f"Cannot convert the given data: expected {'float' if var.dtype == 'int' else 'int'}", column = code.find(dtype.value)))

        return  None

    @staticmethod
    def alu(index, tokens, sign: str = '+'):
        addend_1 = tokens[index - 1]
        addend_2 = tokens[index + 1]

        match addend_1.type:
            case Tokens.INTEGER:
                addend = int(addend_1.value)
            case Tokens.FLOAT:
                addend = float(addend_1.value)
            case Tokens.STRING:
                addend = str(addend_1.value)
            case _:
                addend = None
        match addend_2.type:
            case Tokens.INTEGER:
                addend2 = int(addend_2.value)
            case Tokens.FLOAT:
                addend2 = float(addend_2.value)
            case Tokens.STRING:
                addend2 = str(addend_2.value)
            case _:
                addend2 = None
        if Tokens.is_compatible(addend_1, addend_2):
            if addend_1.type == Tokens.IDENTIFIER:
                addend = Table.variable_table.get(addend_1.value)
                addend = addend.dt_value

            if addend_2.type == Tokens.IDENTIFIER:
                addend2 = Table.variable_table.get(addend_2.value)
                addend2 = addend2.dt_value

            return addend + addend2 if sign == '+' else addend - addend2 if sign == '-' else addend * addend2 if sign == '*' \
                else addend / addend2 if sign == '/' else addend % addend2

        return None

    @staticmethod
    def parse_exp(tokens: list[Tokens.Token]):
        for index in range(len(tokens)):
            token = tokens[index]
            match token.type:
                case Tokens.PLUS:
                    return Parser.alu(index, tokens)
                case Tokens.MINUS:
                    return Parser.alu(index, tokens, sign='-')
                case Tokens.MUL:
                    return Parser.alu(index, tokens, sign='*')
                case Tokens.DIV:
                    return Parser.alu(index, tokens, sign='/')
                case Tokens.MOD:
                    return Parser.alu(index, tokens, sign='%')
        return None
