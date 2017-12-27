from __future__ import absolute_import, print_function

class Token(object):

    def __init__(self, tag:str):
        self.tag = tag

    def to_tuple(self):
        return (None,self.tag,None)

    def __str__(self):
        return self.tag