from __future__ import absolute_import, print_function

class TreeNode(object):
    def __init__(self, data):
        self.sublings = []
        self.child = None
        self.data = data

    def is_leaf(self):
        return True if self.child is None else False

    def gencode(self, symbol_table, code):
        print(self)
        raise NotImplementedError()

    def print(self, indent=''):
        print("{}|-{}".format(indent, str(self.data)))
        # print(self.sublings)
        if self.is_leaf() is False:
            self.child.print("|  "+indent)
        for node in self.sublings:
            node.print(indent)