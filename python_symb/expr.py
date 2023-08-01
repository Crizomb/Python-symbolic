from __future__ import annotations
from tree import Tree
from operator_file import Add, Mul
from operator_file import UnaryOperator, BinOperator
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






