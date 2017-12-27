from __future__ import absolute_import, print_function
from DataStruct.Tree import TreeNode
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
        if self.child is not None:
            self.child.sublings.append(var_decl)
        else:
            self.child = var_decl

        if self.child is not None:
            self.child.sublings.append(proc_decl)
        else:
            self.child = proc_decl

        if self.child is not None:
            self.child.sublings.append(stmt)
        else:
            self.child = stmt

    def build_table(self):
        pass

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

    def print(self, indent=''):
        print("{}|-{}".format(indent, str(self.data)))
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
        print("!")
        exit()
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

class ProcDeclarator(TreeNode):
    def __init__(self, ast_proc_head, ast_subroutine):
        TreeNode.__init__(self, 'ProcDeclarator')
        self.dict = {
            'ProcHead': ast_proc_head,
            'SubRoutine': ast_subroutine
        }
        self.child = ast_proc_head
        self.child.sublings.append(ast_subroutine)

class EmptyStatement(TreeNode):
    def __init__(self):
        TreeNode.__init__(self, 'EmptyStatement')
        self.dict = None


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
