from __future__ import annotations
from tree import Tree
from operator_file import Add, Mul
from operator_file import UnaryOperator, BinOperator, Add, Mul, Min
from typing import List
from symbols import Var
from parse import infix_str_to_postfix


class Expr(Tree):
    def __init__(self, value, children=None):
        super().__init__(value, children if children else [])

    @staticmethod
    def from_postfix_list(postfix: List):

        def aux():
            first = postfix.pop()
            match first:
                case int() | Var():
                    return Tree(first)
                case UnaryOperator():
                    return Tree(first, [aux()])
                case BinOperator():
                    return Tree(first, [aux(), aux()])

        return aux()

    @staticmethod
    def from_infix_str(expr_str):
        expr_rev_polish = infix_str_to_postfix(expr_str)
        return Expr.from_postfix_list(expr_rev_polish)

    def bin_op_constructor(self, other, op):
        match other:
            case Expr():
                return Expr(op, [self, other])
            case Var() | int() | float():
                return Expr(op, [self, Expr(other)])
            case _:
                return ValueError(f'Invalid type for operation: {other} : {type(other)}')

    def __add__(self, other):
        self.bin_op_constructor(other, Add)

    def __mul__(self, other):
        self.bin_op_constructor(other, Mul)

    def __sub__(self, other):
        self.bin_op_constructor(other, Min)


if __name__ == '__main__':
    x, y = Var('x'), Var('y')









