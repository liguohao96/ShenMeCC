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
    if len(arg.files) == 0:
        # no file inputed, files should be a list contains filename
        from_console(grammer=grammer_str)
    else:
        for file_name in arg.files:
            if file_name is not None and path.exists(file_name):
                from_file(file_name)


def from_file(file_name: str):
    file_content = ""
    file = open(file_name)
    lines = file.readlines()
    print("\n"*4)        
    print("test for PCode VM")
    vm = PCodeVM(verbose=True)
    instructs = []
    for line in lines:
        instructs.append(line.split()[:3])
    vm(*instructs)


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
    main(parser.parse_args())
