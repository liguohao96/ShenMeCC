'''
SimpleLexer
'''
from __future__ import absolute_import, print_function

from Lexer.PL0.Keyword import is_keyword, Keyword
from Lexer.PL0.Identifier import Identifier
from Lexer.PL0.Delimiter import Delimiter
from Lexer.PL0.Operator import Operator
from Lexer.PL0.Number import Int, Float
from CompilerException import LexerException
from Lexer.AbstractLexer import AbstractLexer


class Statement(object):
    def __init__(self, init_str: str=""):
        self.statment_str = init_str

    def __index__(self, index: int):
        if index >= len(self.statment_str):
            return ""
        else:
            return self.statment_str[index]

    def __iadd__(self, other: str):
        self.statment_str += other

    def __radd__(self, other):
        self.statment_str += other

    def __add__(self, other: str):
        return self.statment_str + other


class SimpleLexer(AbstractLexer):
    '''
    SimpleLexer
    '''

    def __init__(self):
        AbstractLexer.__init__(self)
        self.statement = ""
        self.index = -1
        self.peek = " "
        self.sym = ""
        self.length = len(self.statement)
        self.error = False
        self.stop = True
        self.line_index = 1
        self.line_character_count = []
        self.line_character_count.append(0)
        self.character_index = 0

    single_character_delimiter = set(['(', ')', ',', ';', '.'])
    single_character_operator = set(['+', '-', '*', '/', '='])
    operator = {
        '<': ['>', '=', ''],
        '>': ['=', ''],
        ':': ['='],
        '+': [''],
        '-': [''],
        '*': [''],
        '/': [''],
        '=': ['']
    }
    skip_character = set([" ", '\n', "\t"])

    def input(self, statement: str):
        if statement is not None and isinstance(statement, str):
            self.statement = statement
        self.stop, self.length = (False, len(self.statement)) if len(
            self.statement) > 0 else (True, -1)
        self.index = -1
        self.character_index = 0
        # self.peek = self.next_character_safe()
        # may cause bug when statement is ""

    def hasnext(self):
        '''
        should continue
        '''
        return not self.error and not self.stop

    def get_int(self):
        '''
        subroutine for int
        '''
        num = int(0)
        if not self.hasnext() or not str.isdigit(self.peek):
            # print("none hasnext {} | isdigit {}".format(self.hasnext(), str.isdigit(self.peek)))
            return None
        while self.hasnext() and str.isdigit(self.peek):
            num = num * 10 + int(self.peek)
            self.peek = self.next_character_safe()
        return num

    def next_character_safe(self):
        '''
        get next character
        '''
        self.index += 1
        ret = " "
        if self.index < len(self.statement):
            ret = self.statement[self.index]
            self.sym += ret
            self.character_index += 1
        self.stop = False if self.index < self.length else True
        # print("{} / {} has next {}".format(self.index, len(self.statement), self.hasnext()))
        return ret

    def next_character(self):
        '''
        get next character
        IndexError may be raised
        '''
        if self.index < len(self.statement):
            self.index += 1
            ret = self.statement[self.index]
            self.sym += ret
            self.character_index += 1
        else:
            self.sym = ""
            self.stop = True
            raise IndexError()
        self.stop = False if self.index < self.length else True
        return ret

    def go_back(self):
        '''
        go back
        '''
        self.index -= 1
        if self.index < len(self.statement):
            # print("restore")
            self.peek = self.statement[self.index]
            self.sym = self.sym[:-1]
            self.character_index -= 1
        self.stop = False if self.index < self.length else True

    def forward(self):
        '''
        get a token or None when done
        '''
        ret = None
        try:
            while (True):
                if self.peek in SimpleLexer.skip_character:
                    if self.peek == '\n':
                        self.line_index += 1
                        self.line_character_count.append(self.character_index)
                        self.character_index = 0
                    self.sym = ""
                    self.peek = self.next_character()
                    continue
                else:
                    break
            if str.isdigit(self.peek):
                num = self.get_int()
                if self.peek == '.':
                    self.peek = self.next_character_safe()
                    float_part = self.get_int()
                    if float_part is not None:
                        self.sym = self.sym[-1]
                        return Float("{}.{}".format(num, float_part))
                    else:
                        self.go_back()
                self.sym = self.sym[-1]
                return Int(num)
            elif str.isalpha(self.peek):
                name = self.peek
                self.peek = self.next_character_safe()
                while str.isalpha(self.peek) or str.isdigit(self.peek):
                    name += self.peek
                    self.peek = self.next_character_safe()
                self.sym = self.sym[-1]
                return Keyword(name) if is_keyword(name) else Identifier(name)
            else:
                if self.peek in SimpleLexer.single_character_delimiter:
                    # 分界符
                    ret = Delimiter(self.peek)
                    self.sym = ""
                    self.peek = self.next_character_safe()
                    return ret
                else:
                    # 运算符
                    if self.peek in SimpleLexer.operator:
                        head_character = self.peek
                        self.peek = self.next_character_safe()
                        if self.peek in SimpleLexer.operator[head_character]:
                            ret = Operator(self.sym)
                            self.sym = ""
                            self.peek = self.next_character_safe()
                            return ret
                        elif '' in SimpleLexer.operator[head_character]:
                            ret = Operator(head_character)
                            self.sym = self.sym[-1]
                            return ret
        except IndexError:
            self.stop = True
            return None
        if self.stop:
            pass
        character_index = 0
        for i in range(self.line_index):
            character_index += self.line_character_count[i]
        display_len = 10 if character_index + \
            10 < len(self.statement) else len(self.statement) - character_index
        error_str = "Error at {0.line_index}:{0.character_index}\n".format(
            self)
        error_str += self.statement[character_index:character_index + display_len]
        error_str += "\n"
        for i in range(self.character_index - 1):
            error_str += "-"
        error_str += "^"
        # raise Exception("Error at {0.line_index}:{0.character_index}".format(self))
        raise LexerException(self.line_index, self.character_index)
