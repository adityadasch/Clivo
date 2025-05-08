import Tokens
from Memory import Table, ClassScope, FunctionScope, Variable, Scope
from Error import RunTimeError, SyntaxError, KeyError, raise_

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
    def parse(tokens: list[Tokens.Token], code, file = 'Console', line = '1'):
        if tokens[-1].type != Tokens.END:
            raise_(SyntaxError(file,line,"Semi-colon is missing", code, column = len(code.rstrip())))
        for index in range(len(tokens)):
            token = tokens[index]
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
                    else:
                        prev = Table.variable_table[token.value].value
                        value = tokens[index + 2].value if Table.variable_table.get(
                            tokens[index + 2].value) is None else Table.variable_table.get(tokens[index + 2].value).value
                        Table.update_variable(token.value, value)
                        print('Updated {} from {} to {}'.format(token.value, prev, value))

                elif len(tokens) > 1 and tokens[index - 1].type == Tokens.DTYPE:
                    dtype = tokens[index - 1].value
                    Table.create_variable(
                        token.value,
                        Tokens.get_default_for_type(dtype),
                        dtype
                    )

                elif len(tokens) > 1 and tokens[index - 1].type == Tokens.KEYWORD:
                    pass
                # else:
                #     variable = Table.variable_table.get(token.value)
                #     print(variable)

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
                    print(Table.variable_table.get(to_show.value))

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
                                print('Checking {}'.format(str(left) + Tokens.COMPARITIVES_DICT.get(ele.type) + str(right)))
                                res = eval(
                                    str(left) + Tokens.COMPARITIVES_DICT.get(ele.type) + str(right)
                                )
                        Table.last_result = res

                elif token.value == 'then':
                    if Table.last_result:
                        Parser.parse(tokens[1::], code, file, line)
                        break

            match token.type:
                case Tokens.PLUS:
                    Parser.alu(index, tokens)
                case Tokens.MINUS:
                    Parser.alu(index, tokens, sign = '-')
                case Tokens.MUL:
                    Parser.alu(index, tokens, sign = '*')
                case Tokens.DIV:
                    Parser.alu(index, tokens, sign='/')

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

            return addend+addend2


        return None


    @staticmethod
    def parse_exp(tokens: list[Tokens.Token]):
        for index in range(len(tokens)):
            token = tokens[index]
            match token.type:
                case Tokens.PLUS:
                    return Parser.alu(index, tokens)
                case Tokens.MINUS:
                    return Parser.alu(index, tokens, sign = '-')
                case Tokens.MUL:
                    return Parser.alu(index, tokens, sign = '*')
                case Tokens.DIV:
                    return Parser.alu(index, tokens, sign='/')
        return None
