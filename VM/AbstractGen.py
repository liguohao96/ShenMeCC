from __future__ import absolute_import, print_function


class AbstractGen(object):
    def __init__(self):
        pass

    def __call__(self, syntax_tree):
        return self.parse(syntax_tree)

    def parse(self, syntax_tree):
        raise NotImplementedError()
