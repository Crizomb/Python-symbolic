from __future__ import annotations

import python_symb.MathTypes.symbols
from python_symb.Expressions.tree import Tree
from python_symb.MathTypes.operator_file import Add, Mul, Min

from python_symb.MathTypes.operator_file import UnaryOperator, BinOperator, Add, Mul, Min

from typing import List
from python_symb.MathTypes.symbols import Var

from python_symb.Parsing.parse import infix_str_to_postfix


class Expr(Tree):
    """
    A class to represent an expression tree

    value: the value of the node
    children: the subtrees of the root (Default : None)

    exemple :
    5*(2+3) represented as
    Expr(Mul, [Expr(5), Expr(Expr(Add, [Expr(2), Expr(3)]))])

    """

    def __init__(self, value, children=None):
        super().__init__(value, children if children else [])

    @staticmethod
    def from_postfix_list(postfix: List):
        """
        Create an expression tree from a postfix list of tokens

        tokens are : int, float, Var, UnaryOperator, BinOperator

        exemple :
        x = Var('x')
        [5, 2, Add] -> Expr(Add, [Expr(5), Expr(2)])
        """

        def aux():
            first = postfix.pop()
            match first:
                case int() | Var():
                    return Expr(first)
                case UnaryOperator():
                    return Expr(first, [aux()])
                case BinOperator():
                    return Expr(first, [aux(), aux()])

        return aux()

    @staticmethod
    def from_infix_str(expr_str) -> Expr:
        """
        Create an expression tree from an infix string
        """
        expr_rev_polish = infix_str_to_postfix(expr_str)
        return Expr.from_postfix_list(expr_rev_polish)

    def bin_op_constructor(self, other, op):
        """
        Construct a binary operation
        """
        match other:
            case Expr():
                return Expr(op, [self, other])
            case Var() | int() | float():
                return Expr(op, [self, Expr(other)])
            case _:
                return ValueError(f'Invalid type for operation: {other} : {type(other)}')

    def __add__(self, other):
        return self.bin_op_constructor(other, Add)

    def __mul__(self, other):
        return self.bin_op_constructor(other, Mul)

    def __sub__(self, other):
        return self.bin_op_constructor(other, Min)


def test1():
    x, y = Var('x'), Var('y')
    expr1 = x + y
    expr2 = 5+x
    print(expr1 + expr2)


def test2():
    from python_symb.MathTypes.operator_file import Sin
    a, b = Var('a'), Var('b')
    expr = Sin(a+b)
    print(expr)


if __name__ == '__main__':
    test1()
    test2()










