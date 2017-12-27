from __future__ import absolute_import, print_function

class TreeNode(object):
    def __init__(self, data):
        self.sublings = []
        self.child = None
        self.data = data

    def is_leaf(self):
        return True if self.child is None else False

    def print(self, indent=''):
        print("{}|-{}".format(indent, str(self.data)))
        if self.is_leaf() is False:
            self.child.print("|  "+indent)
        for node in self.sublings:
            node.print(indent)