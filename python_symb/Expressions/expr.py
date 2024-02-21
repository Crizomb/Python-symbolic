from __future__ import annotations

import python_symb.MathTypes.symbols
from python_symb.Expressions.tree import Tree

from python_symb.MathTypes.operator_file import UnaryOperator, BinOperator, Add, Mul, Exp

from typing import List
from python_symb.MathTypes.symbols import Var, var

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
    __match_args__ = ('value', 'children')

    def __init__(self, value, children=None):
        from python_symb.MathTypes.operator_file import BinOperator, UnaryOperator
        super().__init__(value, children if children else [])
        assert all([isinstance(child, Expr) for child in self.children]), f'Invalid children: {self.children} all child should be Expr'

        match value:
            case BinOperator() as op:
                assert len(self.children) == 2, f'Invalid number of children for BinOperator{op}: {len(self.children)}'

            case UnaryOperator() as op:
                assert len(self.children) == 1, f'Invalid number of children for UnaryOperator{op}: {len(self.children)}'


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


    def to_infix_str(self, parent_precedence=-100, implicit_mul=True) -> str:
        """
        Return the infix string of the expression
        """
        match self:
            case Expr(value) if self.is_leaf:
                return str(value)

            case Expr(UnaryOperator() as op, [child]):
                return f"{op.name}({child.to_infix_str(parent_precedence=op.precedence)})"

            case Expr(BinOperator() as op, [left, right]):
                op_name = op.name if not(implicit_mul and op == Mul) else ''
                if op.precedence < parent_precedence:
                    return f"({left.to_infix_str(op.precedence, implicit_mul)}{op_name}{right.to_infix_str(op.precedence, implicit_mul)})"
                else:
                    return f"{left.to_infix_str(op.precedence, implicit_mul)}{op_name}{right.to_infix_str(op.precedence, implicit_mul)}"




    @staticmethod
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
        other_expr = other if isinstance(other, Expr) else Expr(other)
        return Expr.bin_op_constructor(self, other_expr, Add)

    def __radd__(self, other):
        other_expr = other if isinstance(other, Expr) else Expr(other)
        return Expr.bin_op_constructor(other_expr, self, Add)

    def __mul__(self, other):
        other_expr = other if isinstance(other, Expr) else Expr(other)
        return Expr.bin_op_constructor(self, other_expr, Mul)

    def __rmul__(self, other):
        other_expr = other if isinstance(other, Expr) else Expr(other)
        return Expr.bin_op_constructor(other_expr, self, Mul)

    def __pow__(self, other):
        other_expr = other if isinstance(other, Expr) else Expr(other)
        return Expr.bin_op_constructor(self, other_expr, Exp)

    def __neg__(self):
        return Expr(Mul, [Expr(-1), self])

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __hash__(self):
        """
        Two equivalent expressions (without more modification like factorisation, or expanding) should have the same hash
        see test_eq
        """
        match self:

            case Expr(value) if self.is_leaf:
                return hash(value)

            case Expr(UnaryOperator() as op, [child]):
                return hash(op.name + str(hash(child)))

            case Expr(BinOperator() as op, [left, right]):
                if op.properties.commutative and op.properties.associative:
                    return hash(op.name) + hash(left) + hash(right)
                else:
                    return hash(op.name) + hash(str(hash(left)) + str(hash(right)))

            case _:
                print(f'Invalid type: {type(self)}')

    def bad_eq(self, other):
        return self.__hash__() == other.__hash__()

    def __eq__(self, other):
        """temporary"""
        return self.bad_eq(other)

    def delete_node(self, node: Expr) -> Expr:
        """
        return a new expression without all occurences of the node (with the equality defined by the __eq__ method)

        :param node: node to delete everywhere
        """
        match self:

            case Expr(value) if self.is_leaf:
                if self == node:
                    raise "Cannot delete a leaf node, don't"
                else:
                    return self

            case Expr(UnaryOperator() as op, [child]):
                if child == node:
                    raise ValueError("Cannot delete a node that is the child of a unary operator, don't.")
                else:
                    return Expr(op, [child.delete_node(node)])

            case Expr(BinOperator() as op, [left, right]):
                if left == node:
                    return right
                elif right == node:
                    return left
                else:
                    return Expr(op, [left.delete_node(node), right.delete_node(node)])

            case _:
                raise ValueError(f'Invalid type: {type(self)}')















