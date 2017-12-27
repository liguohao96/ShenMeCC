from __future__ import absolute_import, print_function


class AbstractVM(object):
    def __init__(self):
        pass

    def __call__(self, *code):
        return self.parse(*code)

    def parse(self, *code):
        raise NotImplementedError()
