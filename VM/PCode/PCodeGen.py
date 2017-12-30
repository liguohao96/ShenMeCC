from __future__ import absolute_import, print_function
from VM.AbstractGen import AbstractGen
from CompilerException import SemanticException

class SymbolTable(object):
    def __init__(self):
        self.dict = {}
        self.block_sym = []
    
    def push_block(self, block=None):
        if block is None:
            self.block_sym.append(BlockSymbolTable())
        else:
            self.block_sym.append(block)
    
    def insert(self, table_item):
        if len(table_item) >= 3:
            name = table_item[0]
            item, level, offset = self.search_safe(name)
            if level == 0:
                raise SemanticException('duplicate declaration of {}'.format(name))
                # if item[1] == table_item[1]:
                #     print('[WARNING] duplicate declaration of {}, overwriting'.format(name))
                #     return offset
                # else:
                #     print('[WARNING] change type of {}, from <{}> to <{}>'.format(name, item[1], table_item[1]))
                #     self.block_sym[-1].table[offset] = table_item
                #     return offset
                # self.block_sym[-1][offset] = table_item
            else:
                self.block_sym[-1].append(table_item)
                return -1
        else:
            raise RuntimeError('table item must be at least 3')

    def search_safe(self, name):
        block_chain_len = len(self.block_sym)
        for i in range(block_chain_len):
            block = self[block_chain_len - i - 1]
            for j, item in enumerate(block):
                if item[0] == name:
                    return item, i, j
        return None, -1, -1

    def search(self, name):
        item, level, offset = self.search_safe(name)
        if item is not None:
            return item, level, offset
        raise SemanticException('undefined reference {}'.format(name))

    def pop_block(self):
        self.block_sym.pop()

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.block_sym[index]
        elif isinstance(index, str):
            return self.dict[index]

class BlockSymbolTable(object):
    def __init__(self):
        # table's item should be a (name, type, value)
        self.table = []
    
    def append(self, item):
        self.table.append(item)

    def __iter__(self):
        return self.table.__iter__()
    # def __len__(self):
    #     return len(self.table)

    # def __getitem__(self, item):
    #     if item >= len(self):
    #         raise StopIteration()
    #     else:
    #         return self[item]

class PCodeGener(AbstractGen):
    def __init__(self):
        AbstractGen.__init__(self)
        self.symbol_table = SymbolTable()

    def __call__(self, syntax_tree):
        return self.parse(syntax_tree)

    def parse(self, syntax_tree):
        # self.symbol_table.push_block()
        code = []
        syntax_tree.gencode(self.symbol_table, code)
        return code
