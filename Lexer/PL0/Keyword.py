from __future__ import absolute_import
from Lexer.PL0.Token import Token

keywords = ['const', 'var', 'procedure', 'odd', 'if', 'then', 'while',
            'do', 'call', 'begin', 'end', 'repeat', 'until', 'read', 'write', 'else']

def is_keyword(name:str):
    return True if name in keywords else False

class Keyword(Token):

    def __init__(self, name:str):
        Token.__init__(self, "keyword")
        if name in keywords == False:
            raise Exception("{} is not a keyword".format(name))
        self.value = name

    def to_tuple(self):
        return (self.value, "keyword", self.value)

    def __str__(self):
        return self.value