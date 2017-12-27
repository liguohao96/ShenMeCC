from __future__ import absolute_import, print_function
from VM.AbstratVM import AbstractVM
from VM.PCode import PCodeVM


class PCodeVM(AbstractVM):
    def __init__(self, **keywords):
        AbstractVM.__init__(self)
        self.verbose = False
        if 'verbose' in keywords:
            self.verbose = keywords['verbose']
        self.stack = []
        self.ebp = 0
        self.esp = 0
        self.call_table = {
            'LIT': self.LIT,
            'OPR': self.OPR,
            'LOD': self.LOAD,
            'STO': self.STORE,
            'CAL': self.CALL,
            'INT': self.INT,
            'JMP': self.JUMP,
            'JPC': self.JUMP_CONDITION,
            'RED': self.READ,
            'WRT': self.WRITE
        }
        self.initialize()

    def LIT(self, instruct):
        if int(instruct[1]) == 0:
            self.stack.append(int(instruct[2]))
        self.eip = self.eip + 1

    def OPR(self, instruct):
        self.eip = self.eip + 1

    def LOAD(self, instruct):
        self.eip = self.eip + 1

    def STORE(self, instruct):
        self.eip = self.eip + 1

    def CALL(self, instruct):
        self.eip = self.eip + 1

    def INT(self, instruct):
        self.eip = self.eip + 1

    def JUMP(self, instruct):
        if int(instruct[1]) == 0:
            self.eip = int(instruct[2])
        else:
            self.eip = self.eip + 1

    def JUMP_CONDITION(self, instruct):
        self.eip = self.eip + 1

    def READ(self, instruct):
        self.eip = self.eip + 1

    def WRITE(self, instruct):
        print(self.stack[-1])
        self.eip = self.eip + 1

    def initialize(self):
        self.code, self.stack = [], []
        self.ebp = 0 # B 基地址寄存器
        self.esp = 0 # T 栈顶寄存器
        self.eip = 0 # I 指令寄存器
        self.exit = False

    def parse(self, *code):
        self.code.extend(code)
        while self.exit is False:
            self.single_excute()
        # for i in self.code:
        #     self.single_excute(instruct)
        #     if self.verbose is True:
        #         prt_str = 'instruction {}\n\tstack {}'.format(instruct, self.stack)
        #         print(prt_str)

    def single_excute(self):
        instruct = self.code[self.eip]
        oprand = instruct[0]
        self.call_table[oprand](instruct)
        self.exit = True if self.eip >= len(self.code) else False
        if self.verbose is True:
            prt_str = 'instruction {}\n\tstack {}'.format(instruct, self.stack)
            print(prt_str)
        
