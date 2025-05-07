import Tokens
from Memory import Table, ClassScope, FunctionScope, Variable
from Error import RunTimeError, SyntaxError

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
        tokens.append(Tokens.Token(Tokens.END))
        for index in range(len(tokens)):
            token = tokens[index]
            if token.type == Tokens.EQUAL:
                if tokens[index - 1].type == Tokens.EQUAL:
                    pass
                elif tokens[index - 1].type == Tokens.IDENTIFIER:
                    if Table.variable_table.get(tokens[index - 1].value) is None:
                        value = tokens[index - 2].value if Table.variable_table.get(tokens[index - 1].value) is None else Table.variable_table.get(tokens[index - 1].value).value
                        Table.create_variable(
                            tokens[index - 1].value,
                            tokens[index + 1].value,
                            value
                        )
                    else:
                        prev = Table.variable_table[tokens[index - 1].value].value
                        value = tokens[index + 1].value if Table.variable_table.get(
                            tokens[index + 1].value) is None else Table.variable_table.get(tokens[index + 1].value).value
                        print(value)
                        Table.update_variable(tokens[index - 1].value, value)
                        print('Updated {} from {} to {}'.format(tokens[index - 1].value, prev, value))

            elif tokens[index].type == Tokens.REASSIGN:
                if tokens[index - 1].type == Tokens.IDENTIFIER:
                    if Table.variable_table.get(tokens[index - 1].value).dtype == Table.variable_table[
                        tokens[index + 1].value].dtype:
                        print(tokens[index - 2].value)
                        Table.variable_table[tokens[index - 1].value] = Table.variable_table.get(
                            tokens[index + 1].value)
                    else:
                        return RunTimeError(file, line,
                                            f'Cannot assign {Table.variable_table[tokens[index - 2].value].value} the given value. Convert the value before assigning',
                                            code)
            elif token.type == Tokens.IDENTIFIER:
                if len(tokens) > 1 and tokens[index + 1].type == Tokens.LEFT_PAREN:
                    pass
                elif len(tokens) > 1 and tokens[index - 1].type == Tokens.KEYWORD:
                    pass
                elif len(tokens) > 1 and tokens[index + 1].type == Tokens.EQUAL:
                    pass
                elif len(tokens) > 1 and tokens[index - 1].type == Tokens.ACCESS:
                    variable = Table.variable_table.get(token.value)
                    print(variable)

            elif token.type == Tokens.KEYWORD:
                if token.value == 'func':
                    return_type = tokens[index + 1].value if tokens[index + 1].type == Tokens.KEYWORD else RunTimeError(file,line,'Return type not specified', code)
                    name = tokens[index + 2].value if tokens[index + 1].type == Tokens.KEYWORD else SyntaxError(file,line,'Function name not specified', code)
                    Table.scope_table[name] = FunctionScope()
                    scope = Table.scope_table[name]

                    if tokens[index + 3].type == Tokens.LEFT_PAREN:
                        braces = tokens[index+3::]
                        for i in range(len(braces)):
                            if braces[i].type == Tokens.RIGHT_PAREN:
                                break
                            else:
                                if braces[i].type == Tokens.KEYWORD and braces[i+1].type == Tokens.IDENTIFIER:
                                    scope.arguments[braces[i+1].value] = Variable(
                                        None,
                                        braces[i].value,
                                    )
                                    scope.variables[braces[i+1].value] = scope.arguments.get(braces[i+1].value)

                elif token.value == 'scope':
                    Table.variable_table = dict(Table.variable_table, **Table.scope_table[tokens[index + 1].value].variables)
                    print('Using scoep variables from {}'.format(tokens[index + 1].value))


        return  None
