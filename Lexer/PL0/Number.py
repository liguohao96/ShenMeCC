from __future__ import absolute_import, print_function

from Lexer.PL0.Token import Token


class Int(Token):
    # const var procedure odd if then while do
    # call begin end repeat until read write
    def __init__(self, num:str or int):
        Token.__init__(self, "const int")
        self.value = num if isinstance(num, str) else str(num)

        self.binary = Int.binary_from_decimal(num)

    def binary_from_decimal(num:str or int):
        bits = []
        num = int(num) if isinstance(num, str) else num
        while num/2 != 0:
            bits.append(num%2)
            num=int(num/2)
        bits.reverse()
        bits = [str(b) for b in bits]
        return "".join(bits)

    def to_tuple(self):
        return (self.value, "const int", self.binary)

    def __str__(self):
        return self.value

class Float(Token):
    def __init__(self, num:str or float):
        Token.__init__(self, "const float")
        self.value = str(num)

    def to_tuple(self):
        return (self.value, "const float", self.value)

    def __str__(self):
        return self.value

def binary_from_decimal(num):
    bits = []
    while num/2 != 0:
        bits.append(num%2)
        num=int(num/2)
    bits.reverse()
    ret = "0"
    bits = [str(b) for b in bits]
    return "".join(bits)
    #return ret

if __name__ == "__main__":
    nums = [16,1,0]
    for n in nums:
        print(binary_from_decimal(n))