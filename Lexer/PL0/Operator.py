from __future__ import absolute_import, print_function

from Lexer.PL0.Token import Token


class Operator(Token):
    # const var procedure odd if then while do
    # call begin end repeat until read write
    def __init__(self, name:str):
        Token.__init__(self, "operator")
        self.value = name

    def to_tuple(self):
        return (self.value, "operator", self.value)

    def __str__(self):
        return self.value