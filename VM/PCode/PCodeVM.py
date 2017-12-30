from __future__ import absolute_import, print_function
from VM.AbstratVM import AbstractVM
from VM.PCode import PCodeVM
from CompilerException import RuntimeException


class PCodeVM(AbstractVM):
    def __init__(self, **keywords):
        AbstractVM.__init__(self)
        self.mode = {
            'debug':keywords['debug'] if 'debug' in keywords else False,
            'verbose':keywords['verbose'] if 'verbose' in keywords else False,
            'break_point':-1
        }
        self.stack = []
        self.ebp = 0
        self.esp = -1
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
        self.oprand_table = {
            0:self.ret,
            1:self.opposit,
            2:self.dual_op_func_generator('+'),  # +
            3:self.dual_op_func_generator('-'),  # -
            4:self.dual_op_func_generator('*'),  # *
            5:self.dual_op_func_generator('/'),  # /
            6:self.odd,                          # if stack top is odd
            7:self.dual_cmp_func_generator('=='),   # ==
            8:self.dual_cmp_func_generator('!='),   # !=
            9:self.dual_cmp_func_generator('<'),   # <
            10:self.dual_cmp_func_generator('>='),   # stack[-2] >= stack[-1]
            11:self.dual_cmp_func_generator('>'),   # stack[-2] > stack[-1]
            12:self.dual_cmp_func_generator('<='),   # <=
        }
        self.alias_table={
            'ebp':['ebp', 'B'],
            'esp':['esp', 'T'],
            'eip':['eip', 'P']
        }
        self.initialize()

    def dual_op_func_generator(self, oprand):
        def func():
            op2 = self.pop() # stack top
            op1 = self.pop() # stack sub top
            exec('self.push( int(op1 {} op2) )'.format(oprand))
            self.instruct_human = "{} {} {} -> {}".format(op1, oprand, op2, self.stack[-1])
            self.eip = self.eip + 1
            # self.push(ret)
        return func

    def dual_cmp_func_generator(self, oprand):
        def func():
            op2 = self.pop() # stack top
            op1 = self.pop() # stack sub top
            exec('self.push( 0 if op1 {} op2 else 1)'.format(oprand))
            self.instruct_human = "{} {} {} -> {}".format(op1, oprand, op2, self.stack[-1])
            self.eip = self.eip + 1
            # self.push(ret)
        return func
    
    def gt(self):
        op2 = self.pop()
        op1 = self.pop()
        self.push( 0 if op1 > op2 else 1)
        self.eip = self.eip + 1
    
    def odd(self):
        # test if the stack top is odd(1,3,5)
        self.stack[self.esp] = (self.stack[self.esp] + 1) % 2
        self.eip = self.eip + 1

    def opposit(self):
        self.stack[self.esp] = - self.stack[self.esp]
        self.eip = self.eip + 1

    def ret(self):
        # ret_addr = self.stack[self.ebp + 2]
        self.esp = self.ebp + 2
        self.stack = self.stack[:self.ebp + 3]
        self.eip = self.pop() # pop out RA
        self.ebp = self.pop() # pop out DL
        self.pop() # pop out SL

    def pos(self, level, offset):
        static_chain = self.ebp
        level, offset = int(level), int(offset)
        # print("SL {}|level {} |offset {}".format(static_chain, level, offset))
        for i in range(level):
            # print(static_chain)
            static_chain = self.stack[static_chain]
        static_chain += 3
        pos = static_chain + offset
        return pos

    def pop(self):
        ret = self.stack[self.esp]
        self.stack = self.stack[:self.esp]
        # little bit trick, notice that
        # [1, 2, 3][:2] = [1, 2]
        self.esp -= 1
        return ret
        
    def push(self, data):
        self.stack.append(data)
        self.esp += 1

    def LIT(self, instruct):
        # (LIT, 0, data)
        # push data into stack
        if int(instruct[1]) == 0:
            self.push(int(instruct[2]))
        self.eip = self.eip + 1

    def OPR(self, instruct):
        # (OPR, 0, operand_code)
        if int(instruct[1]) == 0:
            self.oprand_table[int(instruct[2])]()

    def LOAD(self, instruct):
        # (LOD, level, offset)
        # push SL(level)+offset into stack
        pos = self.pos(*instruct[1:])
        self.push(self.stack[pos])
        self.eip = self.eip + 1

    def STORE(self, instruct):
        # (STO, level, offset)
        # store stack top into SL(level)+offset
        pos = self.pos(*instruct[1:])
        # print("[{}] = [{}]".format(pos, self.esp))
        self.stack[pos] = self.stack[self.esp] # or -1
        self.pop()
        self.eip = self.eip + 1
        

    def CALL(self, instruct):
        # (CAL, level, abs_func_pos)
        # call function at abs_func_pos, build SL, DL, RA in stack
        static_chain = self.ebp
        for i in range(int(instruct[1])):
            static_chain = self.stack[static_chain]
        self.stack.append(static_chain) # static chain
        self.stack.append(self.ebp) # dynamic chain
        self.eip = self.eip + 1
        self.stack.append(self.eip)
        func_pos = int(instruct[2])
        # print("[{}] code {}".format(func_pos, self.code[func_pos]))
        # print("SL:{}|DL:{}|RA:{}".format(static_chain, self.ebp, self.eip))
        self.ebp = self.esp + 1
        self.esp = self.ebp + 2
        self.eip = func_pos

    def INT(self, instruct):
        # (INT, 0, x)
        # append current stack for x times
        if int(instruct[1]) == 0:
            times = int(instruct[2])
            self.stack.extend([0]*times)
            self.esp += times
        self.eip = self.eip + 1

    def JUMP(self, instruct):
        # (JMP, 0, abs_pos)
        # jump to abs_pos of code, without condition
        if int(instruct[1]) == 0:
            self.eip = int(instruct[2])
            # print("jump to [{}] [{}]".format(self.eip, self.code[self.eip]))
        else:
            self.eip = self.eip + 1

    def JUMP_CONDITION(self, instruct):
        # (JMP, 0, abs_pos)
        # jump to abs_pos of code, only if the stack top is 0
        if int(instruct[1]) == 0:
            if self.stack[self.esp] == 0:
                # jump
                self.eip = int(instruct[2])
            else:
                self.eip = self.eip + 1
            self.pop()

    def READ(self, instruct):
        # (RED, level, offset)
        # read input, store at SL(level)+offset
        pos = self.pos(*instruct[1:])
        if 0 <= pos < len(self.stack):
            pass
        else:
            self.panic('try to read at {}'.format(pos))
        # print("READ pos {}".format(pos))
        read_done = False
        while read_done is False:
            ipt = input("input>")
            try:
                self.stack[pos] = int(ipt)
                read_done = True
            except:
                print('input error')
        self.eip = self.eip + 1

    def WRITE(self, instruct):
        # (WRT, 0, 0)
        # output stack top
        print(self.stack[self.esp]) # -1 is ok for representing the last one
        self.pop()
        self.eip = self.eip + 1

    def initialize(self):
        self.code, self.stack = [], [0, 0, 0]
        self.ebp = 0 # B 基地址寄存器
        self.esp = 2 # T 栈顶寄存器
        self.eip = 0 # I 指令寄存器
        self.mode['break_point'] = -1
        self.exit = False
        self.instruct_human = None

    def panic(self, panic_msg):
        raise RuntimeException(panic_msg)

    def print_stack(self, pos=None):
        if pos is not None:
            print('stack[{}] is [{}]'.format(pos, self.stack[pos]))
        else:
            stack_str = ""
            pos_index = {}
            pos_each = 5
            for i in range(len(self.stack)):
                if i%pos_each == 0:
                    pos_index[len(stack_str)] = str(i)
                if i == self.ebp:
                    pos_index[len(stack_str)] = "B"
                if i == self.esp:
                    pos_index[len(stack_str)] = "T"
            # pos_index[self.esp] = 'T'
                stack_str += "|{}".format(self.stack[i])
            index = 0
            i = 0
            header = ""
            while index < len(stack_str):
                if index in pos_index:
                    num_str = pos_index[index]
                    header += num_str
                    # print(num_str, end='')
                    index += len(num_str)
                else:
                    header += " "
                    # print(" ", end='')
                    index += 1
            # print()
            header_str = " "
            for c in header:
                header_str += "\u0332{}".format(c)
            # print("_"*len(stack_str))
            print(header_str)
            print(stack_str)
            print(" \u0305"*len(stack_str))
            # print('x\u0305\u0332x\u0305\u0332x\u0305\u0332x\u0332')
            # print("1\u0305\u0332")
            

    def command_promt(self, *done_str):
        ipt = input('>')
        while ipt not in done_str:
            try:
                ipt_splited = ipt.split()
                op_code = ipt_splited[0]
                if op_code == 'i':
                    instruct_idx = int(ipt.split()[1])
                    print(self.code[instruct_idx])
                if op_code == 'b':
                    instruct_idx = int(ipt.split()[1])
                    self.mode['break_point'] = instruct_idx
                if op_code == 'mode':
                    name = ipt.split()[1]
                    print('{}:{}'.format(name, self.mode[name]))
                if op_code == 'stack':
                    pos = int(ipt_splited[1]) if len(ipt_splited) >= 2 else None
                    self.print_stack(pos)
                if op_code == 'exit':
                    exit()
                if op_code in self.alias_table['ebp']:
                    print("{}: {}".format(op_code, self.ebp))
                if op_code in self.alias_table['esp']:
                    print("{}: {}".format(op_code, self.esp))
                if op_code in self.alias_table['eip']:
                    print("{}: {}".format(op_code, self.eip))
                if op_code in self.call_table:
                    if len(ipt.split()) >= 3:
                        self.instruct_excute(ipt.split()[:3])
            except Exception as ex:
                pass
            ipt = input('>')

    def parse(self, *code):
        # code = [ (c[0], int(c[1]), int(c[2])) for c in code]
        self.code.extend(code)
        if self.mode['verbose'] is True or self.mode['debug'] is True:
            prt_str = 'stack {}'.format(self.stack)
            print(prt_str)
        if self.mode['debug'] is True:
            self.command_promt('r')
            self.mode['debug'] = False
        while self.exit is False:
            if self.eip == self.mode['break_point']:
                self.mode['debug'] = True
            
            if self.mode['debug'] is True:
                print("to excute [{}] {}".format(self.eip, self.code[self.eip]))
                self.command_promt('n', '')

            instruct = self.code[self.eip]
            eip = self.eip
            self.instruct_excute(instruct)

            if self.mode['debug'] is True:
                print_instruct = self.instruct_human if self.instruct_human is not None else instruct
                prt_str = 'instruction {}: {}\nstack {}\n eip :{}'.format(eip+1, print_instruct, self.stack, self.eip)
                self.instruct_human = None
                print(prt_str)

            if self.mode['verbose'] is True and not self.mode['debug']:
                print_instruct = self.instruct_human if self.instruct_human is not None else instruct
                prt_str = '\tinstruction {}: {}\nstack {}\n eip :{}'.format(eip+1, print_instruct, self.stack, self.eip)
                self.instruct_human = None
                print(prt_str)
            self.exit = True if self.eip >= len(self.code) else False
            
            # print(self.stack)
        # for i in self.code:
        #     self.single_excute(instruct)
        #     if self.verbose is True:
        #         prt_str = 'instruction {}\n\tstack {}'.format(instruct, self.stack)
        #         print(prt_str)

    def instruct_excute(self, instruct):
        oprand = instruct[0]
        self.call_table[oprand](instruct)
        
    
    def core_dump(self):
        print("core dump")
        print("ebp:{}| esp:{}| eip:{}".format(self.ebp, self.esp, self.eip))
        print(self.stack)
