class Error:
    def __init__(self, file, line, message, code):
        self.file = file
        self.line = line
        self.message = message
        self.code = code
    def __repr__(self):
        return f'''{self.__class__.__name__} in {self.file}: At {self.line} \n \t {self.code}\n {self.message}'''

class SyntaxError(Error):
    def __init__(self, file, line, message, code):
        super().__init__(file, line, message, code)

class RunTimeError(Error):
    def __init__(self, file, line, message, code):
        super().__init__(file, line, message, code)