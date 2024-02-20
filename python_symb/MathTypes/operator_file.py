from __future__ import annotations
from typing import Dict, Callable
from python_symb.MathTypes.symbols import Symbols


class Operator(Symbols):
    """
    Represent an operator, like +, *, sin, anything that can be applied to an expression
    """
    instances = {}

    def __init__(self, name: str, precedence: int, call: Callable, repeated_op: Operator = None):
        """
        :param name of the operator
        :param precedence: precedence of the operator, higher is better
        :param call: function to apply the operator
        :param repeated_op: if you repeat the operator what do you get ?
        for exemple a+a+a+a -> 4*a, the repeated_op of Add is Mul
        """

        super().__init__(name)
        self.precedence = precedence
        self.call = call
        self.repeated_op = repeated_op
        Operator.instances[name] = self

    def __repr__(self):
        return f'{self.name}'


class UnaryOperator(Operator):
    """
    Represent a unary operator, like sin, cos, - etc...
    all operators that take only one argument
    """
    instances = {}

    def __init__(self, name: str, precedence: int, call: Callable, repeated_op: Operator = None):
        UnaryOperator.instances[name] = self
        super().__init__(name, precedence, call, repeated_op)

    def apply(self, expr):
        return self.call(expr)

    def __call__(self, e):
        from python_symb.Expressions.expr import Expr
        return Expr(self, [e])


class BinProperties:
    """
    Represent the properties of a binary operator
    """

    def __init__(self, associativity: bool, commutativity: True,
                 left_distributivity: Dict[str, bool], right_distributivity: Dict[str, bool]):
        """
        :param associativity: True if the operator is associative
        :param commutativity: True if the operator is commutative
        :param left_distributivity: a dictionary of the operators that the current operator distribute over
        :param right_distributivity: a dictionary of the operators that distribute over the current operator

        exemple:
        for the operator *:
        associativity = True
        commutativity = True
        left_distributivity = {'+': True}
        right_distributivity = {'+': True}
        """

        self.associativity = associativity
        self.commutativity = commutativity
        self.left_distributivity = left_distributivity
        self.right_distributivity = right_distributivity


class BinOperator(Operator):
    """
    Represent a binary operator, like +, *, etc...
    all operators that take two arguments
    """

    # Used to store all the instances of BinOperator, used in the parser
    instances = {}

    def __init__(self, name: str, precedence: int, properties: BinProperties, call: Callable, repeated_op: Operator = None ):
        BinOperator.instances[name] = self
        super().__init__(name, precedence, call, repeated_op)
        self.properties = properties

    def apply(self, left, right):
        return self.call(left, right)


"""
Generic operators
"""

AddProperties = BinProperties(True, True, {'*': True}, {'*': True})
Add = BinOperator('+', 2, AddProperties, lambda x, y: x + y)


MulProperties = BinProperties(True, True, {'+': True}, {'+': True})
Mul = BinOperator('*', 3, MulProperties, lambda x, y: x * y)
Sin = UnaryOperator('sin', 10, lambda x: x)

Min = BinOperator('-', 2, AddProperties, lambda x, y: x - y)


