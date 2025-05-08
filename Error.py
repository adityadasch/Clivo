from direct.directtools.DirectSelection import SelectionSegment


class Error:
    def __init__(self, file, line, message, code, **kwargs):
        self.file = file
        self.line = line
        self.message = message
        self.code = code
        self.column = kwargs.get('column')
    def __repr__(self):
        return f'''{self.__class__.__name__} in {self.file}: At {self.line} \n \t {self.code}\n {self.message}''' if self.column is None else\
    f'{self.__class__.__name__} in {self.file}: At {self.line} \n \t {self.code}\n \t {' '*self.column+'^'}\n {self.message}'

class SyntaxError(Error):
    def __init__(self, file, line, message, code, **kwargs):
        super().__init__(file, line, message, code, **kwargs)

class RunTimeError(Error):
    def __init__(self, file, line, message, code, **kwargs):
        super().__init__(file, line, message, code, **kwargs)

class KeyError(Error):
    def __init__(self, file, line, message, code, **kwargs):
        super().__init__(file, line, message, code, **kwargs)

class DataTypeError(Error):
    def __init__(self, file, line, message, code, **kwargs):
        super().__init__(file, line, message, code, **kwargs)

def raise_(error: Error):
    print(error)
    quit()