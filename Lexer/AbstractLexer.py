from __future__ import absolute_import, print_function

class AbstractLexer(object):

    def __init__(self):
        pass

    def input(self, source:str):
        raise NotImplementedError()

    def hasnext(self):
        raise NotImplementedError()

    def forward(self):
        raise NotImplementedError()
    
    def backward(self):
        raise NotImplementedError()