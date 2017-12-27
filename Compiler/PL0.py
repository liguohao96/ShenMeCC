'''
demo of compiler
'''
from __future__ import absolute_import, print_function
import sys
import os.path as path
sys.path.append('.')
from Lexer import PL0Lexer as Lexer
from CompilerException import LexerException

def main():
    '''
    main test code
    '''
    file_name = sys.argv[1] if len(sys.argv) > 1 else None
    if file_name is not None and path.exists(file_name):
        from_file(file_name)
    else:
        from_console()
    
def from_file(file_name:str):
    file_content = ""
    lexer = Lexer()
    file = open(file_name)
    lines = file.readlines()
    for line in lines:
        file_content += line
    lexer.input(file_content)
    print(lexer.statement)
    print("{:8}|{:10}|{:>10}".format("单词", "类别", "值"))
    while lexer.hasnext():
        try:
            ret = lexer.scan()
            if ret is not None:
                print("{0[0]:10}|{0[1]:12}|{0[2]:>10}".format(ret.to_tuple()))
        except LexerException as ex:
            lexer.peek = lexer.next_character_safe()
            print(ex)
            print(lines[ex.line_index - 1], end='')
            point_str = ""
            for i in range(ex.character_index - 1):
                point_str += "-"
            point_str += "^"
            print(point_str)

def from_console():
    lexer = Lexer()
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
                    print("{0[0]:10}|{0[1]:12}|{0[2]:>10}".format(ret.to_tuple()))
            except LexerException as ex:
                lexer.peek = lexer.next_character_safe()
                print(ex)
                print(input_str, end='\n')
                point_str = ""
                for i in range(ex.character_index - 1):
                    point_str += "-"
                point_str += "^"
                print(point_str)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='lexer for PL0(i don\'t know what it is.)')
    # parser.add_argument("-f", "--file-name", type=str, default=None, help="input file")
    # main(parser.parse_args())
    main()
