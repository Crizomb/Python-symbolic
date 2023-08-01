from __future__ import annotations
from typing import List, Union
from operator_file import Add, Mul, Min, BinOperator, UnaryOperator
from symbols import Symbols, Var
from fraction import Fraction

x, y = Var('x'), Var('y')

ParenthesisLeft = Symbols('(')
ParenthesisRight = Symbols(')')

Number = Union[int, float, Fraction]

name_to_symbol = {sy.name:sy for sy in Symbols.instances}

print(name_to_symbol)

"""
example1 = "a + b * c + d"
-
example2 = 2*x+3*y*(4+sin(5))
-
example3 = "(a + b) * (c + -d))"
should return Tree(Expr('*', [Expr('+', [Expr('a'), Expr('b')]), Expr('+', [Expr('c'), Expr('-', [Expr('d')])])]))
"""


def preprocess(expr: str) -> List:
    """
    Preprocesses a string expression to a list of symbols and numbers
    :param expr: string expression
    :return: list of symbols and numbers
    """
    return_list = []
    expr = expr.strip()
    expr = expr.replace(' ', '')
    m = max([len(sy) for sy in name_to_symbol.keys()])
    i = 0
    while i < len(expr):
        found = False
        for j in range(m, 0, -1):
            word = expr[i:i+j]
            if word in name_to_symbol or word.isdigit():
                if word in name_to_symbol:
                    return_list.append(name_to_symbol[word])
                else:
                    return_list.append(int(word))
                i += j
                found = True
                break

        if not found:
            raise ValueError(f'Invalid expression: {expr} at index {i}\n')
    return return_list


def return_to_string(expr: List) -> str:
    """
    Returns a string expression from a list of symbols and numbers
    :param expr: list of symbols and numbers
    :return: string expression
    """
    return ' '.join([str(sy) for sy in expr])


def infix_to_postfix(expr: List) -> List:
    global ParenthesisLeft, ParenthesisRight
    """
    Converts an infix string expression (standard) to a postfix expression (reverse polish notation)
    :param expr: infix expression
    :return: postfix expression

    use shunting yard algorithm
    """
    op_stack = []
    postfix = []
    for sy in expr:
        match sy:
            case int() | float() | Fraction() | Var():
                postfix.append(sy)
            case _ if sy == ParenthesisLeft:
                op_stack.append(sy)
            case _ if sy == ParenthesisRight:
                while op_stack[-1] != ParenthesisLeft:
                    postfix.append(op_stack.pop())
                op_stack.pop()
            case UnaryOperator():
                op_stack.append(sy)
            case BinOperator():
                while op_stack and op_stack[-1] != ParenthesisLeft and op_stack[-1].precedence >= sy.precedence:
                    postfix.append(op_stack.pop())
                op_stack.append(sy)
    while op_stack:
        postfix.append(op_stack.pop())
    return postfix


def infix_str_to_postfix(expr):
    return infix_to_postfix(preprocess(expr))


if __name__ == "__main__":

    expr = "(x+7)*y+sin(24-2*(1-5))"
    prep = preprocess(expr)
    print(prep)
    post = infix_to_postfix(prep)
    print(post)
    print(return_to_string(post))





