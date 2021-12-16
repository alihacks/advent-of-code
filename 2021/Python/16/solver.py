from typing import List
import binascii
import math

class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 20
        self.test2 = 1
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr) -> List:
        self.data = ""
        for c in list(instr.strip()):
            self.data += bin(int(c, 16))[2:].zfill(4)

    def take(self, n):
        res = self.data[self.i : self.i + n]
        self.i += n
        return res

    def read_packet(self):
        ver = self.take(3)
        typ = self.take(3)
        read_count = 6
        # print("   V=", ver, "T=", typ)
        self.part1 += int(ver, 2)
        if typ == "100":  # literal
            done = False
            num = ""
            while not done:
                grp = self.take(5)
                read_count += 5
                num += grp[1:]
                done = grp[0] == "0"
            return int(num,2)
        else:  # operator
            len_type = self.take(1)
            op = int(typ, 2)
            vals = []
            if len_type == "0":  # next 15 bits = total_len
                len_to_read = int(self.take(15), 2)
                stop_at = self.i + len_to_read
                while self.i < stop_at:
                    vals.append(self.read_packet())
            else:  # next 11 bits = num_packets
                packets_to_read = int(self.take(11), 2)
                for _ in range(packets_to_read):
                    vals.append(self.read_packet())

            #print("Operator:", op, "with vals=", vals)
            match op:
                case 0:
                    res = sum(vals)
                case 1:
                    res = math.prod(vals)
                case 2:
                    res = min(vals)
                case 3:
                    res = max(vals)
                case 5:
                    res = 1 if vals[0] > vals[1] else 0
                case 6:
                    res = 1 if vals[0] < vals[1] else 0
                case 7:
                    res = 1 if vals[0] == vals[1] else 0
                case _:
                    assert(False)
        return res

    def process(self):
        self.i = 0

        self.part2 = self.read_packet()

    def solve(self):
        self.part1 = 0
        self.process()
