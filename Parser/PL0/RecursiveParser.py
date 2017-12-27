from __future__ import absolute_import, print_function
from Parser.AbstractParser import AbstractParser
from Lexer.PL0.Keyword import is_keyword, Keyword
from Lexer.PL0.Identifier import Identifier
from Lexer.PL0.Delimiter import Delimiter
from Lexer.PL0.Operator import Operator
from Lexer.PL0.Number import Int, Float
from Lexer.AbstractLexer import AbstractLexer
from DataStruct.Tree import TreeNode
from DataStruct import SyntaxTree
from CompilerException import LexerException

from VM.PCode import PCodeVM
class RecursiveParser(AbstractParser):

    def __init__(self, lexer: AbstractLexer):
        AbstractParser.__init__(self)
        self.lexer = lexer
        self.token = None

    def grammer_input(self, grammer: str):
        grammer = grammer.split('\n')
        Vn_dict = {}
        for g in grammer:
            g = g[:-1] if g[-1] == '\r' else g
            g = g.strip()
            vn, sentences = g.split('::=')
            if vn not in Vn_dict:
                Vn_dict[vn] = [sentences]
            else:
                Vn_dict[vn].append(sentences)
        print(Vn_dict)

    def parse(self, source: str):
        self.lexer.input(source)
        self.token = self.lexer.forward()
        try:
            anal_tree, syntax_tree = self.程序()
            anal_tree.print('')
            print("!!!!!!!")
            syntax_tree.print()
        except LexerException as ex:
            print(ex)
            print(source.split('\n')[ex.line_index - 1])
            # ex.line_index
        
        # tree = self.分程序()
        # tree.print('')
        while self.lexer.hasnext():
            # print("[{}/{}] {}".format(self.lexer.index, len(source), source[self.lexer.index:]))
            pass

    def 程序(self):
        sub_tree = TreeNode('<程序>')
        child_tree, syntax_tree = self.分程序()
        if isinstance(self.token, Delimiter) and self.token.value == '.':
            child_tree.sublings.append(TreeNode(self.token))
            self.token = self.lexer.forward()
            sub_tree.child = child_tree
            return sub_tree, syntax_tree

    def 分程序(self):
        sub_tree = TreeNode('<分程序>')
        child_tree, ast_const_decl, ast_var_decl, ast_proc_decl, ast_smnt_tree = None, None, None, None, None
        if isinstance(self.token, Keyword) and self.token.value == 'const':
            child_tree, ast_const_decl = self.常量说明部分()
        if isinstance(self.token, Keyword) and self.token.value == 'var':
            anal_var_decl, ast_var_decl = self.变量说明部分()
            if child_tree is None:
                child_tree = anal_var_decl
            else:
                child_tree.sublings.append(anal_var_decl)
        if isinstance(self.token, Keyword) and self.token.value == 'procedure':
            anal_proc_decl, ast_proc_decl = self.过程说明部分()
            if child_tree is None:
                child_tree = anal_proc_decl
            else:
                child_tree.sublings.append(anal_proc_decl)
        anal_smnt_tree, ast_smnt_tree = self.语句()
        if child_tree is None:
            child_tree = anal_smnt_tree
        else:
            child_tree.sublings.append(anal_smnt_tree)
        sub_tree.child = child_tree
        ast_tree = SyntaxTree.SubRoutine(const_decl=ast_const_decl, var_decl=ast_var_decl, proc_decl=ast_proc_decl,
                                         stmt=ast_smnt_tree)
        return sub_tree, ast_tree
    
    def 常量说明部分(self):
        analysis_tree = TreeNode('<常量说明部分>')
        syntax_tree = SyntaxTree.ConstDeclaration()
        if isinstance(self.token, Keyword) and self.token.value == 'const':
            child_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            const_def, syntax_constdef = self.常量定义()
            syntax_tree.insert(syntax_constdef)
            child_tree.sublings.append(const_def)
            while isinstance(self.token, Delimiter) and self.token.value == ',':
                child_tree.sublings.append(TreeNode(self.token))
                self.token = self.lexer.forward()
                const_def, syntax_constdef = self.常量定义()
                syntax_tree.insert(syntax_constdef)
                child_tree.sublings.append(const_def)
            else:
                if isinstance(self.token, Delimiter) and self.token.value == ';':
                    child_tree.sublings.append(TreeNode(self.token))
                    self.token = self.lexer.forward()
                    analysis_tree.child = child_tree
                    return analysis_tree, syntax_tree

    def 常量定义(self):
        analysis_tree = TreeNode('<常量定义>')
        child_tree, syntax_indentifier = self.标识符()
        if isinstance(self.token, Operator) and self.token.value == '=':
            child_tree.sublings.append(TreeNode(self.token))
            self.token = self.lexer.forward()
            subling, syntax_int = self.无符号整数()
            child_tree.sublings.append(subling)
            analysis_tree.child = child_tree
            syntax_tree = SyntaxTree.ConstDeclarator(syntax_indentifier, syntax_int)
            return analysis_tree, syntax_tree

    def 无符号整数(self):
        sub_tree = TreeNode('<无符号整数>')
        if isinstance(self.token, Int):
            sub_tree.child = TreeNode(self.token)
            syntax_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            return sub_tree, syntax_tree

    def 标识符(self):
        sub_tree = TreeNode('<标识符>')
        if isinstance(self.token, Identifier):
            sub_tree.child = TreeNode(self.token)
            syntax_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            return sub_tree, syntax_tree

    def 变量说明部分(self):
        sub_tree = TreeNode('<变量说明部分>')
        variable_declarator = []
        if isinstance(self.token, Keyword) and self.token.value == 'var':
            child_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            identifier, syntax_identifier = self.标识符()
            variable_declarator.append(syntax_identifier)
            child_tree.sublings.append(identifier)
            while isinstance(self.token, Delimiter) and self.token.value == ',':
                child_tree.sublings.append(TreeNode(self.token))
                self.token = self.lexer.forward()
                identifier, syntax_identifier = self.标识符()
                variable_declarator.append(syntax_identifier)
                child_tree.sublings.append(identifier)
            else:
                if isinstance(self.token, Delimiter) and self.token.value == ';':
                    child_tree.sublings.append(TreeNode(self.token))
                    syntax_tree = SyntaxTree.VariableDeclaration(*variable_declarator)
                    self.token = self.lexer.forward()
                    sub_tree.child = child_tree
                    return sub_tree, syntax_tree

    def 过程说明部分(self):
        sub_tree = TreeNode('<过程说明部分>')
        child_tree, ast_proc_head = self.过程首部()
        seperate_prog, ast_subroutine = self.分程序()
        child_tree.sublings.append(seperate_prog)
        proc_decl = SyntaxTree.ProcDeclarator(ast_proc_head, ast_subroutine)
        addtion_proc_decl = [proc_decl]
        if isinstance(self.token, Delimiter) and self.token.value == ';':
            child_tree.sublings.append(self.token)
            self.token = self.lexer.forward()
        while isinstance(self.token, Keyword) and self.token.value == 'procedure':
            anal_proc_decl, ast_proc_decl = self.过程说明部分()
            ast_proc_decl = ast_proc_decl.dict['Declarations']
            addtion_proc_decl.extend(ast_proc_decl)
            child_tree.sublings.append(anal_proc_decl)
        else:
            # child_tree.sublings.append(TreeNode(self.token))
            # self.token = self.lexer.forward()
            # sub_tree.child = child_tree
            ast_tree = SyntaxTree.ProcDeclaration(*addtion_proc_decl)
            return sub_tree, ast_tree

    def 过程首部(self):
        sub_tree = TreeNode('<过程首部>')
        if isinstance(self.token, Keyword) and self.token.value == 'procedure':
            child_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            identifier, ast_indetifier = self.标识符()
            if identifier is not None:
                child_tree.sublings.append(identifier)
                if isinstance(self.token, Delimiter) and self.token.value == ';':
                    child_tree.sublings.append(TreeNode(self.token))
                    self.token = self.lexer.forward()
                    sub_tree.child = child_tree
                    return sub_tree, ast_indetifier


    def 语句(self):
        sub_tree = TreeNode('<语句>')
        if isinstance(self.token, Identifier):
            # assginment
            child_tree, syntax_tree = self.赋值语句()
            sub_tree.child = child_tree
            # syntax_tree.print()
            return sub_tree, syntax_tree
        call_tab = {
            'if':self.条件语句,
            'while':self.当型循环语句,
            'call':self.过程调用语句,
            'read':self.读语句,
            'write':self.写语句,
            'begin':self.复合语句,
            'repeat':self.重复语句,
        }
        if isinstance(self.token, Keyword) and self.token.value in call_tab:
            # print("选择 {}".format(self.token.value))
            child_tree, syntax_tree = call_tab[self.token.value]()
            sub_tree.child = child_tree
            return sub_tree, syntax_tree
        else:
            sub_tree.child = TreeNode("")
            return sub_tree, SyntaxTree.EmptyStatement()

    def 赋值语句(self):
        sub_tree = TreeNode('<赋值语句>')
        child_tree, ast_identifier_lhs = self.标识符()
        if isinstance(self.token, Operator) and self.token.value == ':=':
            child_tree.sublings.append(TreeNode(self.token))
            self.token = self.lexer.forward()
            expression, ast_identifier_rhs = self.表达式()
            child_tree.sublings.append(expression)
            sub_tree.child = child_tree
            syntax_tree = SyntaxTree.AssignExpression(ast_identifier_lhs, ast_identifier_rhs)
            return sub_tree, syntax_tree

    def 表达式(self):
        sub_tree = TreeNode('<表达式>')
        child_tree = None
        heading_operator = None
        syntax_tree = None
        if isinstance(self.token, Operator) and self.token.value in ['+', '-']:
            # TODO
            child_tree = TreeNode(self.token)
            heading_operator = self.token.value
            self.token = self.lexer.forward()
        anal_term, ast_term = self.项()
        if child_tree is not None:
            child_tree.sublings.append(anal_term)
        else:
            child_tree = anal_term
        if heading_operator is None or heading_operator in ['+']:
            syntax_tree = ast_term
        else:
            ast_heading_zero = TreeNode(Int(0))
            syntax_tree = SyntaxTree.BinaryExpression(heading_operator, ast_heading_zero, ast_term)
        while isinstance(self.token, Operator) and self.token.value in ['+', '-']:
            anal_add, ast_add = self.加法运算符()
            child_tree.sublings.append(anal_add)
            anal_term, rhs_term = self.项()
            syntax_tree = SyntaxTree.BinaryExpression(ast_add, syntax_tree, rhs_term)
            child_tree.sublings.append(anal_term)
        else:
            sub_tree.child = child_tree
            return sub_tree, syntax_tree

    def 项(self):
        sub_tree = TreeNode('<项>')
        child_tree, ast_tree = self.因子()
        while isinstance(self.token, Operator) and self.token.value in ['*', '/']:
            anal_mul, ast_mul = self.乘法运算符()
            child_tree.sublings.append(anal_mul)
            fractor, ast_fractor = self.因子()
            ast_tree = SyntaxTree.BinaryExpression(ast_mul, ast_tree, ast_fractor)
            child_tree.sublings.append(fractor)
        else:
            sub_tree.child = child_tree
            return sub_tree, ast_tree

    def 因子(self):
        sub_tree = TreeNode('<因子>')
        if isinstance(self.token, Identifier):
            sub_tree.child = TreeNode(self.token)
            syntax_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            return sub_tree, syntax_tree
        if isinstance(self.token, Int):
            sub_tree.child = TreeNode(self.token)
            syntax_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            return sub_tree, syntax_tree
        if isinstance(self.token, Delimiter) and self.token.value == '(':
            child_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            expression = self.表达式()
            child_tree.sublings.append(expression)
            if isinstance(self.token, Delimiter) and self.token.value == ')':  
                child_tree.sublings.append(TreeNode(self.token))
                sub_tree.child = child_tree
                self.token = self.lexer.forward()
                return sub_tree

    def 加法运算符(self):
        sub_tree = TreeNode('<加法运算符>')
        if isinstance(self.token, Operator):
            if self.token.value == '+' or self.token.value == '-':
                child_tree = TreeNode(self.token)
                self.token = self.lexer.forward()
                sub_tree.child = child_tree
                return sub_tree, child_tree.data.value

    def 乘法运算符(self):
        sub_tree = TreeNode('<乘法运算符>')
        if isinstance(self.token, Operator):
            if self.token.value == '*' or self.token.value == '/':
                child_tree = TreeNode(self.token)
                self.token = self.lexer.forward()
                sub_tree.child = child_tree
                return sub_tree, child_tree.data.value

    def 条件(self):
        sub_tree = TreeNode('<条件>')
        syntax_tree = None
        if isinstance(self.token, Keyword) and self.token.value == 'odd':
            child_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            expression, ast_expression = self.表达式()
            syntax_tree = SyntaxTree.OddStatement(ast_expression)
        else:
            expression, ast_lhs = self.表达式()
            child_tree = expression
            operator, ast_operator = self.关系运算符()
            child_tree.sublings.append(operator)
            expression, ast_rhs = self.表达式()
            syntax_tree = SyntaxTree.BinaryExpression(ast_operator, ast_lhs, ast_rhs)
        child_tree.sublings.append(expression)
        sub_tree.child = child_tree
        return sub_tree, syntax_tree

    def 关系运算符(self):
        sub_tree = TreeNode('<关系运算符>')
        if isinstance(self.token, Operator):
            if self.token.value in ['=', '<>', '<', '<=', '>', '>=']:
                child_tree = TreeNode(self.token)
                self.token = self.lexer.forward()
                sub_tree.child = child_tree
                return sub_tree, child_tree.data.value

    def 条件语句(self):
        sub_tree = TreeNode('<条件语句>')
        syntax_tree = None
        if isinstance(self.token, Keyword) and self.token.value == 'if':
            child_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            condition, ast_condition = self.条件()
            child_tree.sublings.append(condition)
            if isinstance(self.token, Keyword) and self.token.value == 'then':
                child_tree.sublings.append(TreeNode(self.token))
                self.token = self.lexer.forward()
                statment, ast_true_stmt = self.语句()
                child_tree.sublings.append(statment)
                ast_false_stmt = SyntaxTree.EmptyStatement()
                if isinstance(self.token, Keyword) and self.token.value == 'else':
                    child_tree.sublings.append(TreeNode(self.token))
                    self.token = self.lexer.forward()
                    statment, ast_false_stmt = self.语句()
                    
                    child_tree.sublings.append(statment)
                sub_tree.child = child_tree
                syntax_tree = SyntaxTree.IfStatement(ast_condition, ast_true_stmt, false_stmt=ast_false_stmt)
                return sub_tree, syntax_tree

    def 当型循环语句(self):
        sub_tree = TreeNode('<当型循环语句>')
        if isinstance(self.token, Keyword) and self.token.value == 'while':
            child_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            condition, ast_condition = self.条件()
            child_tree.sublings.append(condition)
            if isinstance(self.token, Keyword) and self.token.value == 'do':    
                child_tree.sublings.append(TreeNode(self.token))
                self.token = self.lexer.forward()
                statement, ast_stmt = self.语句()
                child_tree.sublings.append(statement)
                sub_tree.child = child_tree
                syntax_tree = SyntaxTree.WhileStatement(condition=ast_condition, statement=ast_stmt)
                return sub_tree, syntax_tree
    def 过程调用语句(self):
        sub_tree = TreeNode('<过程调用语句>')
        if isinstance(self.token, Keyword) and self.token.value == 'call':
            child_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            identifier, ast_identifier = self.标识符()
            if identifier is not None:
                child_tree.sublings.append(identifier)
                sub_tree.child = child_tree
                syntax_tree = SyntaxTree.CallExpression(identifier=ast_identifier)
                return sub_tree, syntax_tree

    def 复合语句(self):
        sub_tree = TreeNode('<复合语句>')
        ast_stmt_list = []
        if isinstance(self.token, Keyword) and self.token.value == 'begin':
            child_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            statement, ast_stmt = self.语句()
            child_tree.sublings.append(statement)
            ast_stmt_list.append(ast_stmt)
            while isinstance(self.token, Delimiter) and self.token.value == ';':
                child_tree.sublings.append(TreeNode(self.token))
                self.token = self.lexer.forward()
                statement, ast_stmt = self.语句()
                child_tree.sublings.append(statement)
                ast_stmt_list.append(ast_stmt)
            else:
                if isinstance(self.token, Keyword) and self.token.value == 'end':
                    child_tree.sublings.append(TreeNode(self.token))
                    self.token = self.lexer.forward()
                    sub_tree.child = child_tree
                    syntax_tree = SyntaxTree.BlockStatement(*ast_stmt_list)
                    return sub_tree, syntax_tree

    def 重复语句(self):
        sub_tree = TreeNode('<重复语句>')
        stmt_list = []
        if isinstance(self.token, Keyword) and self.token.value == 'repeat':
            child_tree = TreeNode(self.token)
            self.token = self.lexer.forward()
            statement, ast_statement = self.语句()
            stmt_list.append(ast_statement)
            child_tree.sublings.append(statement)
            while isinstance(self.token, Delimiter) and self.token.value == ';':
                child_tree.sublings.append(TreeNode(self.token))
                self.token = self.lexer.forward()    
                statement, ast_statement = self.语句()
                stmt_list.append(ast_statement)
                child_tree.sublings.append(statement)
            else:
                if isinstance(self.token, Keyword) and self.token.value == 'until':
                    child_tree.sublings.append(TreeNode(self.token))
                    self.token = self.lexer.forward()
                    condition, ast_condition = self.条件()
                    child_tree.sublings.append(condition)
                    sub_tree.child = child_tree
                    syntax_tree = SyntaxTree.DoWhileStatement(condition=ast_condition, statement=stmt_list)

                    return sub_tree, syntax_tree
        #return sub_tree

    def 读语句(self):
        sub_tree = TreeNode('<读语句>')
        if isinstance(self.token, Keyword) and self.token.value == 'read':
            io_type = TreeNode(self.token) 
            child_tree = TreeNode(self.token)
            sub_tree.child = child_tree
            self.token = self.lexer.forward()
            ast_args = self.rw_arg(child_tree)
            syntax_tree = SyntaxTree.IOStatement(io_type, ast_args)
            syntax_tree.print()
            return sub_tree, syntax_tree

    def 写语句(self):
        sub_tree = TreeNode('<写语句>')
        if isinstance(self.token, Keyword) and self.token.value == 'write':
            io_type = TreeNode(self.token) 
            child_tree = TreeNode(self.token)
            sub_tree.child = child_tree
            self.token = self.lexer.forward()
            ast_args = self.rw_arg(child_tree)
            syntax_tree = SyntaxTree.IOStatement(io_type, ast_args)
            syntax_tree.print()
            return sub_tree, syntax_tree
    
    
    def 数字(self):
        pass

    def 字母(self):
        pass

    def narg(self, child_tree, function):
        identifier, ast_identifier = function()
        args_list = []
        if identifier is not None:
            args_list.append(ast_identifier)
            child_tree.sublings.append(identifier)
            while isinstance(self.token, Delimiter) and self.token.value == ',':
                child_tree.sublings.append(TreeNode(self.token))
                self.token = self.lexer.forward()
                identifier, ast_identifier = function()
                #print("!!!!!!!")
                #identifier.print()
                if identifier is not None:
                    child_tree.sublings.append(identifier)
                    args_list.append(ast_identifier)
            else:
                return args_list

    def rw_arg(self, child_tree):
        if isinstance(self.token, Delimiter) and self.token.value == '(':
            child_tree.sublings.append(TreeNode(self.token))
            self.token = self.lexer.forward()
            args_list = self.narg(child_tree, self.标识符)
            if isinstance(self.token, Delimiter) and self.token.value == ')':
                child_tree.sublings.append(TreeNode(self.token))
                self.token = self.lexer.forward()
                syntax_tree = SyntaxTree.Arguments(*args_list)
                return syntax_tree