import Tokens
from Memory import Table
from Error import RunTimeError

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
                elif tokens[index - 1].type == Tokens.COLON:
                    if tokens[index - 2].type == Tokens.IDENTIFIER:
                        if  token_to_dtype(tokens[index + 1].type) == Table.variable_table[tokens[index - 2].value].dtype:
                                Table.variable_table[tokens[index - 2].value].value = tokens[index + 1].value
                        else:
                            return RunTimeError(file,line,f'Cannot assign {Table.value_table[Table.variable_table[tokens[index - 2].value]].value} the given value. Convert the value before assigning', code)
                elif tokens[index - 1].type == Tokens.IDENTIFIER:
                    Table.create_variable(
                        tokens[index - 1].value,
                        tokens[index + 1].value,
                        tokens[index - 2].value
                    )
                    print('Created!')
                    print(Table.variable_table)
            elif token.type == Tokens.IDENTIFIER:
                if len(tokens) > 1 and tokens[index + 1].type == Tokens.LEFT_PAREN:
                    pass
                elif len(tokens) > 1 and tokens[index - 1].type == Tokens.KEYWORD:
                    pass
                elif len(tokens) > 1 and tokens[index + 1].type == Tokens.EQUAL:
                    pass
                elif len(tokens) > 1 and tokens[index - 1].type == Tokens.ACCESS:
                    variable = Table.variable_table.get(tokens[index].value)
                    print(variable.value)
        return  None
