from __future__ import absolute_import, print_function


class AbstractParser(object):
    def __init__(self):
        pass

    def __call__(self, source: str):
        return self.parse(source)

    def parse(self, source: str):
        raise NotImplementedError()
