class LexerException(Exception):
    def __init__(self, line_index:int, character_index:int):
        Exception.__init__(self, Exception)
        self.line_index = line_index
        self.character_index = character_index
    def __str__(self):
        return "Error at {0.line_index}:{0.character_index}".format(self)

class ParserException(Exception):
    def __init__(self, message):
        Exception.__init__(self, Exception)
        self.message = message

    def __str__(self):
        return self.message

class SyntaxException(Exception):
    def __init__(self, message):
        Exception.__init__(self, Exception)
        self.message = message

    def __str__(self):
        return self.message

class SemanticException(Exception):
    def __init__(self, message):
        Exception.__init__(self, Exception)
        self.message = message

    def __str__(self):
        return self.message

        