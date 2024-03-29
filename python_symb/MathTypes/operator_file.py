from __future__ import annotations
from typing import Set, Callable
from python_symb.MathTypes.symbols import Symbols


class Operator(Symbols):
    """
    Represent an operator, like +, *, sin, anything that can be applied to an expression
    """
    # Store all the instances of Operator, used in the parser
    instances = {}
    # The deconstruct operator of a repeated operator is used to deconstruct an expression (x+y)^2 -> (x+y)*(x+y)
    # Mul is the deconstruct operator of Add
    deconstruct_op_dict = {}

    def __init__(self, name: str, precedence: int, call: Callable, repeated_op: BinOperator = None):
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

        if repeated_op:
            Operator.deconstruct_op_dict[repeated_op] = self

    def __repr__(self):
        return f'{self.name}'

    @property
    def deconstruct_op(self):
        return Operator.deconstruct_op_dict.get(self, None)


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

    def __init__(self, associative: bool, commutative: True,
                 left_distributivity: Set[str], right_distributivity: Set[str], neutral_element=None, absorbing_element=None):
        """
        :param associative: True if the operator is associative
        :param commutative: True if the operator is commutative
        :param left_distributivity: a dictionary of the operators that the current operator distribute over
        :param right_distributivity: a dictionary of the operators that distribute over the current operator

        exemple:
        for the operator *:
        associativity = True
        commutativity = True
        left_distributivity = {'+': True}
        right_distributivity = {'+': True}
        """

        self.associative = associative
        self.commutative = commutative
        self.left_distributive = left_distributivity
        self.right_distributive = right_distributivity
        self.neutral_element = neutral_element
        self.absorbing_element = absorbing_element


class BinOperator(Operator):
    """
    Represent a binary operator, like +, *, etc...
    all operators that take two arguments

    """

    # Used to store all the instances of BinOperator, used in the parser
    instances = {}

    def __init__(self, name: str, precedence: int, properties: BinProperties, call: Callable, repeated_op: BinOperator = None):
        """
        :param name: name of the operator
        :param precedence: precedence of the operator, higher is better
        :param properties: properties of the operator
        :param call: function to apply the operator
        :param repeated_op: if you repeat the operator what do you get ? (for exemple a+a+a+a -> 4*a, the repeated_op of Add is Mul)
        :param deconstruct_op: if you deconstruct the operator what do you get ? (for exemple 4*a -> a+a+a+a, the deconstruct_op of Mul is Add)
        """
        BinOperator.instances[name] = self
        super().__init__(name, precedence, call, repeated_op)
        self.properties = properties

    def apply(self, left, right):
        return self.call(left, right)






"""
Generic operators
"""
ExpProperties = BinProperties(False, False, set(), set(), 1)
Exp = BinOperator('^', 4, ExpProperties, lambda x, y: x ** y)

MulProperties = BinProperties(True, True, {'+'}, {'+'}, 1, 0)
Mul = BinOperator('*', 3, MulProperties, lambda x, y: x * y, Exp)

AddProperties = BinProperties(True, True, set(), set(), 0)
Add = BinOperator('+', 2, AddProperties, lambda x, y: x + y, Mul)





Sin = UnaryOperator('sin', 10, lambda x: x)


