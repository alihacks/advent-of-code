from typing import List
import copy

def do_op(l,r,op, reverse = False):
    if reverse:
        op = {'+':'-', '-':'+','*':'/', '/':'*'}[op]
    if op == '+':
        return l + r
    elif op == '-':
        return l - r
    elif op == '*':
        return l * r
    elif op == '/':
        return l // r
        
class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 152
        self.test2 = 301

    def parse(self, instr: str) -> List:
        self.vals = {}
        self.ops = {}
        for parts in [line.split(' ') for line in instr.splitlines()]:
            name = parts[0][:-1]
            if len(parts) == 2:
                self.vals[name] = int(parts[1])
            else:
                self.ops[name] = tuple(parts[1:])


    def calc(self, p2 = False):
        ops = copy.deepcopy(self.ops)
        vals = copy.deepcopy(self.vals)
        if p2:
            del vals['humn']
        while ops:
            progress = False
            for name, (left, op, right) in ops.items():
                if left in vals and right in vals:
                    vals[name] = do_op(vals[left],vals[right],op)
                    del ops[name]
                    progress = True
                    break
            if not progress:
                break
        if p2:
            for name, (left, op, right) in ops.items():
                if left in vals:
                    ops[name] = (vals[left],op,right)
                elif right in vals:
                    ops[name] = (left,op,vals[right])
        return ops, vals

    def solve(self):
        self.part1 = self.calc()[1]['root']

        o, v = self.calc(True)
        left, _, right = o['root']

        res = left if left in v else right
        eq = o[left] if left in o else o[right]


        def simplify(res, l, r, op):
            if isinstance(r,int):
                return do_op(res,r,op, True)
            elif isinstance(l,int):
                if op == '-':
                    return l - res
                return do_op(res,l,op, True)              

        #solve eq
        while True:
            l,op,r = eq
            res = simplify(res,l,r,op)
            if isinstance(r,int):
                eq = o[l]
            elif isinstance(l,int):
                eq = o[r]
            if 'humn' in eq:
                self.part2 = simplify(res, eq[0],eq[2],eq[1])
                break
