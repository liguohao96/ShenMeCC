'''
demo of compiler
'''
from __future__ import absolute_import, print_function
import sys
import os.path as path
from CompilerException import LexerException
from Lexer.PL0 import SimpleLexer as PL0Lexer
from Parser.PL0 import RecursiveParser as PL0Parser
import argparse

from VM import PCodeVM

PL0Compiler = [PL0Lexer, PL0Parser]

def main(arg):
    '''
    main test code
    '''
    grammer_str = ""
    if arg.grammer is not None:
        with open(arg.grammer, 'rb') as f:
            ret = f.read()
            # print(ret)
            grammer_str = ret.decode('utf-8')
            # grammer_str = ret
    else:
        grammer_str = None
    if len(arg.files) == 0:
        # no file inputed, files should be a list contains filename
        from_console(grammer=grammer_str)
    else:
        for file_name in arg.files:
            if file_name is not None and path.exists(file_name):
                from_file(file_name, grammer=grammer_str)

    
    print("\n"*4)        
    print("test for PCode VM")
    vm = PCodeVM(verbose=True)
    vm(('push', 1), ('push', 2))

def from_file(file_name: str, grammer:str=None):
    file_content = ""
    lexer = PL0Lexer()
    parser = PL0Parser(lexer)
    if grammer is not None:
        parser.grammer_input(grammer)
    file = open(file_name)
    lines = file.readlines()
    for line in lines:
        file_content += line
    parser.parse(file_content)
    # print(lexer.statement)
    # print("{:8}|{:10}|{:>10}".format("单词", "类别", "值"))
    # while lexer.hasnext():
    #     try:
    #         ret = lexer.scan()
    #         if ret is not None:
    #             print("{0[0]:10}|{0[1]:12}|{0[2]:>10}".format(ret.to_tuple()))
    #     except LexerException as ex:
    #         lexer.peek = lexer.next_character_safe()
    #         print(ex)
    #         print(lines[ex.line_index - 1], end='')
    #         point_str = ""
    #         for i in range(ex.character_index - 1):
    #             point_str += "-"
    #         point_str += "^"
    #         print(point_str)


def from_console(grammer:str=None):
    lexer = PL0Lexer()
    parser = PL0Parser(lexer)
    while(True):
        input_str = input('>')
        lexer.input(input_str)
        # print("{0.index}/{0.length}".format(lexer))
        while lexer.hasnext():
            try:
                ret = lexer.scan()
                # print(lexer.peek.encode())
                # print("{0.index}/{0.length}".format(lexer))
                if ret is not None:
                    print("{0[0]:10}|{0[1]:12}|{0[2]:>10}".format(
                        ret.to_tuple()))
            except LexerException as ex:
                lexer.peek = lexer.next_character_safe()
                print(input_str, end='\n')
                point_str = ""
                for i in range(ex.character_index - 1):
                    point_str += "-"
                point_str += "^"
                print(point_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='compiler for PL0(i don\'t know what it is.)')
    parser.add_argument("files", type=str, nargs='*', default=[], help='input file', metavar="filename")
    parser.add_argument("-g", "--grammer", type=str, default=None, help="grammer file")
    main(parser.parse_args())
