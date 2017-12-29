from __future__ import absolute_import, print_function
from DataStruct.Tree import TreeNode
import Lexer.PL0 as lexer
from CompilerException import SemanticException
import copy


class SubRoutine(TreeNode):
    def __init__(self, const_decl=None, var_decl=None, proc_decl=None, stmt=None):
        TreeNode.__init__(self, 'SubRoutine')
        self.dict = {
            'ConstDeclaration': const_decl,
            'VariableDeclaration': var_decl,
            'ProcDeclaration': proc_decl,
            'Statement': stmt
        }
        if const_decl is not None:
            self.child = const_decl
        if var_decl is not None:
            if self.child is not None:
                self.child.sublings.append(var_decl)
            else:
                self.child = var_decl
        if proc_decl is not None:
            if self.child is not None:
                self.child.sublings.append(proc_decl)
            else:
                self.child = proc_decl
        if stmt is not None:
            if self.child is not None:
                self.child.sublings.append(stmt)
            else:
                self.child = stmt

    def build_table(self):
        pass

    def gencode(self, symbol_table, code):
        symbol_table.push_block()
        if self.dict['ConstDeclaration'] is not None:
            self.dict['ConstDeclaration'].gencode(symbol_table, code)
        
        if self.dict['VariableDeclaration'] is not None:
            self.dict['VariableDeclaration'].gencode(symbol_table, code)

        if self.dict['ProcDeclaration'] is not None:
            # jump begin procdeclaration
            code.append(['JMP', 0, -1])
            backfill_index = len(code) - 1
            self.dict['ProcDeclaration'].gencode(symbol_table, code)
            code[backfill_index][2] = len(code)
        self.dict['Statement'].gencode(symbol_table, code)
        symbol_table.pop_block()

class ConstDeclaration(TreeNode):
    def __init__(self):
        TreeNode.__init__(self, 'ConstDeclaration')
        self.child = None
        self.dict = {
            'Declarations': []
        }

    def insert(self, *args):
        self.dict['Declarations'].extend(args)
        if self.child is None:
            self.child = args[0]
            if len(args) > 1:
                self.child.sublings.extend(args[1:])
        else:
            self.child.sublings.extend(args)

    def gencode(self, symbol_table, code):
        const_decls = self.dict['Declarations']
        for i, item in enumerate(const_decls):
            name = item.dict['Identifier'].data.value
            value = item.dict['Number'].data.value
            symbol_table.block_sym[-1].append((name, 'const', value))
            instruct = ('LIT', 0, value)
            code.append(instruct)

class ConstDeclarator(TreeNode):
    def __init__(self, identifier, number):
        TreeNode.__init__(self, 'ConstDeclarator')
        self.dict = {
            'Identifier': identifier,
            'Number': number
        }
        self.child = copy.deepcopy(identifier)
        self.child.sublings.append(number)

    def print(self, indent=''):
        print("{}|-{}".format(indent, str(self.data)))
        if self.is_leaf() is False:
            self.dict['Identifier'].print(
                "{}| {}:".format(indent, 'Identifier'))
            self.dict['Number'].print("{}| {}:".format(indent, 'Number'))
            #print("{}| {}:{}".format(indent, 'Number', self.dict['Number']))
            # self.child.print("{}| {}:".format(indent, 'Var'))
        for node in self.sublings:
            # print("!!!!!!!!!")
            # print("{}{}".format(indent, 'Declaration'))
            # exit()
            node.print(indent)


class VariableDeclaration(TreeNode):
    def __init__(self, *args):
        #super(TreeNode, self).__init__('VariableDeclaration')
        TreeNode.__init__(self, 'VariableDeclaration')
        self.dict = {
            'Declarations': args
        }
        self.child = args[0]
        if len(args) > 1:
            self.child.sublings.extend(args[1:])

    def gencode(self, symbol_table, code):
        var_decls = self.dict['Declarations']
        for i, item in enumerate(var_decls):
            name = item.data.value
            symbol_table.block_sym[-1].append((name, 'var', None))
            instruct = ('LIT', 0, 0)
            code.append(instruct)

    def print(self, indent=''):
        print("{}|-{}".format(indent, str(self.data)))
        print(self.sublings)
        if self.is_leaf() is False:
            self.child.print("{}| {}:".format(indent, 'Var'))
        for node in self.sublings:
            # print("!!!!!!!!!")
            # print("{}{}".format(indent, 'Declaration'))
            # exit()
            node.print(indent)


class VariableDeclarator(TreeNode):
    def __init__(self, identifier):
        TreeNode.__init__(self, 'VaraibleDeclarator')
        self.dict = {
            'Identifier': identifier
        }
        self.child = identifier

    def print(self, indent=''):
        print("{}|{}:{}".format(indent, 'Var', str(self.data)))
        if self.is_leaf() is False:
            self.child.print("|  " + indent)
        for node in self.sublings:
            # print("!!!!!!!!!")
            # print("{}{}".format(indent, 'Declaration'))
            # exit()
            node.print(indent)


class ProcDeclaration(TreeNode):
    '''
    <过程说明部分> ::= <过程首部><分程序>{;<过程说明部分>};
    '''

    def __init__(self, *args):
        TreeNode.__init__(self, 'ProcDeclaration')
        self.dict = {
            'Declarations': args
        }
        self.child = args[0]
        if len(args) > 1:
            self.child.sublings.extend(args[1:])
    
    def gencode(self, symbol_table, code):
        proc_decls = self.dict['Declarations']
        for i, item in enumerate(proc_decls):
            name = item.dict['ProcHead'].data.value
            symbol_table.block_sym[-1].append((name, 'proc', len(code)))
            # the first statement is the next one
            item.gencode(symbol_table, code)
            # code.append(('OPR', 0, 0))

class ProcDeclarator(TreeNode):
    def __init__(self, ast_proc_head, ast_subroutine):
        TreeNode.__init__(self, 'ProcDeclarator')
        self.dict = {
            'ProcHead': ast_proc_head,
            'SubRoutine': ast_subroutine
        }
        self.child = ast_proc_head
        self.child.sublings.append(ast_subroutine)
    
    def gencode(self, symbol_table, code):
        sub_routine = self.dict['SubRoutine']
        sub_routine.gencode(symbol_table, code)
        code.append(('OPR', 0, 0))

class EmptyStatement(TreeNode):
    def __init__(self):
        TreeNode.__init__(self, 'EmptyStatement')
        self.dict = None
    
    def gencode(self, symbol_table, code):
        pass


class Arguments(TreeNode):
    def __init__(self, *arg_list):
        TreeNode.__init__(self, 'Arguments')
        self.dict = {
            'Arguments': arg_list
        }
        self.child = arg_list[0]
        if len(arg_list) > 1:
            self.child.sublings.extend(arg_list[1:])


class OddStatement(TreeNode):
    '''
    <条件> ::= odd <表达式>
    '''

    def __init__(self, expression):
        TreeNode.__init__(self, 'OddStatement')
        self.dict = {
            'Expression': expression
        }
        self.child = expression


class BinaryExpression(TreeNode):
    def __init__(self, oprator, lhs, rhs):
        TreeNode.__init__(self, oprator)
        self.dict = {
            'Lhs': lhs,
            'Rhs': rhs
        }
        self.child = copy.deepcopy(lhs)
        self.child.sublings.append(rhs)
    oprator_to_code = {
        '+':('OPR', 0, 2),
        '-':('OPR', 0, 3),
        '*':('OPR', 0, 4),
        '/':('OPR', 0, 5),
        '==':('OPR', 0, 7),
        '!=':('OPR', 0, 8),
        '<':('OPR', 0, 9),
        '>=':('OPR', 0, 10),
        '>':('OPR', 0, 11),
        '<=':('OPR', 0, 12),
    }
    def gencode(self, symbol_table, code):
        insert = BinaryExpression.oprator_to_code[self.data]
        # print(insert)
        if isinstance(self.dict['Lhs'], BinaryExpression):
            self.dict['Lhs'].gencode(symbol_table, code)
        else:
            if isinstance(self.dict['Lhs'].data, lexer.Identifier):
                name = self.dict['Lhs'].data.value
                item, level, offset = symbol_table.search(name)
                if item[1] in ['var', 'const']:
                    code.append(('LOD', level, offset))
                else:
                    raise SemanticException("{} get type <{}>, but expect <var> <const> in [{}]".format(name, item[1], self.data))
            else:
                code.append(('LIT', 0, self.dict['Lhs'].data.value))

        if isinstance(self.dict['Rhs'], BinaryExpression):
            self.dict['Rhs'].gencode(symbol_table, code)
        else:
            if isinstance(self.dict['Rhs'].data, lexer.Identifier):
                name = self.dict['Rhs'].data.value
                item, level, offset = symbol_table.search(name)
                if item[1] in ['var', 'const']:
                    code.append(('LOD', level, offset))
                else:
                    raise SemanticException("{} get type <{}>, but expect <var> <const> in [{}]".format(name, item[1], self.data))
            else:
                code.append(('LIT', 0, self.dict['Rhs'].data.value))
            # print(self.dict['Rhs'])
        code.append(insert)

    def print(self, indent=''):
        print("{}|{}".format(indent, self.data))
        if self.is_leaf() is False:
            # self.child.print("|  "+indent)
            print("{}|  {}:".format(indent, 'lhs'))
            self.dict['Lhs'].print("{}|  ".format(indent))
            print("{}|  {}:".format(indent, 'rhs'))
            self.dict['Rhs'].print("{}|  ".format(indent))
        for node in self.sublings:
            # print("!!!!!!!!!")
            # print("{}{}".format(indent, 'Declaration'))
            # exit()
            node.print(indent)


class AssignExpression(TreeNode):
    '''
    <赋值语句> ::= <标识符>:=<表达式>
    '''

    def __init__(self, lhs, rhs):
        TreeNode.__init__(self, 'AssignExpression')
        self.dict = {
            'Lhs': lhs,
            'Rhs': rhs
        }
        self.child = copy.deepcopy(lhs)
        self.child.sublings.append(rhs)

    def gencode(self, symbol_table, code):
        
        if isinstance(self.dict['Rhs'], BinaryExpression):
            self.dict['Rhs'].gencode(symbol_table, code)
        else:
            if isinstance(self.dict['Rhs'].data, lexer.Number.Int):
                code.append(('LIT', 0, self.dict['Rhs'].data.value))
            elif isinstance(self.dict['Rhs'].data, lexer.Identifier):
                item, level, offset = symbol_table.search(self.dict['Rhs'].data.value)
                if item[1] in ['var', 'const']:
                    code.append(('LOD', level, offset))
            print(type(self.dict['Rhs'].data))
            self.dict['Rhs'].print()

        level, offset = 0, 0
        table_len = len(symbol_table.block_sym)
        for i in range(table_len):
            for j, item in enumerate(symbol_table[table_len - i - 1]):
                name = item[0]
                # print(self.dict['Lhs'])
                if name == self.dict['Lhs'].data.value:
                    if item[1] == 'var':
                        level = i
                        offset = j
                            # print("level {}| offset {}".format(level, offset))
                        code.append(('STO', level, offset))
                        return 
                    else:
                        raise SemanticException("get type <{}>, but expect <var> in [Assign]".format(item[1]))
        raise SemanticException('undefined reference for {}'.format(self.dict['Lhs'].data.value))
    def print(self, indent=''):
        print("{}|{}".format(indent, ':='))
        if self.is_leaf() is False:
            # self.child.print("|  "+indent)
            print("{}|  {}:".format(indent, 'lhs'))
            self.dict['Lhs'].print("{}|  ".format(indent))
            print("{}|  {}:".format(indent, 'rhs'))
            self.dict['Rhs'].print("{}|  ".format(indent))
        for node in self.sublings:
            # print("!!!!!!!!!")
            # print("{}{}".format(indent, 'Declaration'))
            # exit()
            node.print(indent)


class IfStatement(TreeNode):
    '''
    <条件语句> ::= if<条件>then<语句>[else<语句>]
    '''

    def __init__(self, condition, true_stmt, false_stmt=EmptyStatement()):
        TreeNode.__init__(self, 'IfStatement')
        self.dict = {
            'Condition': condition,
            'TrueStatement': true_stmt,
            'FalseStatement': false_stmt
        }
        self.child = condition
        self.child.sublings.append(true_stmt)
        self.child.sublings.append(false_stmt)


class WhileStatement(TreeNode):
    '''
    <当型循环语句> ::= while<条件>do<语句>
    '''

    def __init__(self, condition=None, statement=None):
        TreeNode.__init__(self, 'WhileStatement')
        self.dict = {
            'Condition': condition,
            'Statement': statement
        }
        self.child = condition
        self.child.sublings.append(statement)


class DoWhileStatement(TreeNode):
    '''
    <重复语句> ::= repeat<语句>{;<语句>}until<条件>
    '''

    def __init__(self, condition=None, statement=None):
        TreeNode.__init__(self, 'DoWhileStatement')
        self.dict = {
            'Condition': condition,
            'Statement': statement
        }
        self.child = condition
        self.child.sublings.extend(statement)


class CallExpression(TreeNode):
    '''
    <过程调用语句> ::= call <标识符>
    '''

    def __init__(self, identifier, *arguments):
        TreeNode.__init__(self, 'CallExpression')
        self.dict = {
            'Identifier': identifier,
            'Arguments': arguments,
        }
        self.child = identifier
        if arguments is not None and len(arguments) > 0:
            self.child.sublings.append(arguments)

    def gencode(self, symbol_table, code):
        block_chain_len = len(symbol_table.block_sym)
        for i in range(block_chain_len):
            block = symbol_table[block_chain_len - i - 1]
            for j, item in enumerate(block):
                if item[0] == self.dict['Identifier'].data.value:
                    if item[1] == 'proc':
                        # print('level {}'.format(i))
                        code.append(('CAL', i, item[2]))
                        return 
                    else:
                        raise SemanticException("get type <{}>, but expect <procedure> in call".format(item[1]))
        raise SemanticException('undefined reference {}'.format(self.dict['Identifier'].data.value))

class IOStatement(TreeNode):
    '''
    <读语句> ::= read'('<标识符>{,<标识符>}')'
    <写语句> ::= write'('<标识符>{,<标识符>}')'
    '''

    def __init__(self, io_type, arguments: Arguments):
        TreeNode.__init__(self, 'IOStatement')
        self.dict = {
            'IOType': io_type,
            'Arguments': arguments
        }
        self.child = io_type
        self.child.sublings.append(arguments)

    def gencode(self, symbol_table, code):
        # code_start = len(code) - 1
        iotype = self.dict['IOType'].data.value
        args = [self.dict['Arguments'].child.data.value]
        item, level, offset = symbol_table.search(args[0])
        if iotype == 'write':
            if item[1] != 'proc':
                code.append(('LOD', level, offset))
                code.append(('WRT', 0, 0))
            else:
                raise SemanticException("get type <{}>, but expect <var> or <const>".format(item[1]))
        elif iotype == 'read':
            if item[1] == 'var':
                code.append(('RED', level, offset))
            else:
                raise SemanticException("get type <{}>, but expect <var>".format(item[1]))

        other_args = [ arg.data.value for arg in self.dict['Arguments'].child.sublings]
        args.extend(other_args)
        last_args = args[0]
        for i, arg_name in enumerate(other_args):
            item, level, offset = symbol_table.search(arg_name)
            if iotype == 'write':
                if item[1] != 'proc':
                    if arg_name != last_args:
                        # reduce code length by removing duplicated LOD
                        code.append(('LOD', level, offset))
                        last_args = arg_name
                    code.append(('WRT', 0, 0))
                else:
                    raise SemanticException("get type <{}>, but expect <var> or <const> in write()".format(item[1]))
            elif iotype == 'read':
                if item[1] == 'var':
                    if arg_name == last_args:
                        # duplicated read operation
                        print('[WARING] duplicated read operation')
                    last_args = arg_name
                    code.append(('RED', level, offset))
                else:
                    raise SemanticException("get type <{}>, but expect <var> in read".format(item[1]))

class BlockStatement(TreeNode):
    '''
    <复合语句> ::= begin<语句>{;<语句>}end
    '''

    def __init__(self, *stmt_list):
        TreeNode.__init__(self, 'BlockStatement')
        self.dict = {
            'StatementList': stmt_list
        }
        self.child = stmt_list[0]
        if len(stmt_list) > 1:
            self.child.sublings.extend(stmt_list[1:])

    def gencode(self, symbol_table, code):
        # make block have it's own block
        # JMP to (CAL, 0, len(code))

        # symbol_table.push_block()
        # code.append(['JMP', 0, -1])
        backfill_index = len(code) - 1
        stmt_list = self.dict['StatementList']
        for i, item in enumerate(stmt_list):
            item.gencode(symbol_table, code)

        # code.append(('OPR', 0, 0))
        # code.append(('CAL', 0, backfill_index + 1))
        # code[backfill_index][2] = len(code)-1
        # symbol_table.pop_block()