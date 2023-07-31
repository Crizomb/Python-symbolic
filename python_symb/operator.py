from __future__ import annotations
from typing import Dict, Callable


class Operator:
    __slots__ = 'name', 'precedence', 'call'

    def __init__(self, name: str, precedence: int, call: Callable):
        self.name = name
        self.precedence = precedence
        self.call = call


class UnaryOperator(Operator):
    __slots__ = 'name', 'precedence'

    def __init__(self, name: str, precedence: int, call: Callable):
        super().__init__(name, precedence, call)

    def __call__(self, expr):
        return self.call(expr)


class BinProperties:
    __slots__ = 'associativity', 'commutativity', 'left_distributivity', 'right_distributivity'

    def __init__(self, associativity: bool, commutativity: True,
                 left_distributivity: Dict[str, bool], right_distributivity: Dict[str, bool]):

        self.associativity = associativity
        self.commutativity = commutativity
        self.left_distributivity = left_distributivity
        self.right_distributivity = right_distributivity


class BinOperator(Operator):
    __slots__ = 'name', 'precedence', 'properties'

    def __init__(self, name: str, precedence: int, properties: BinProperties, call: Callable):
        super().__init__(name, precedence, call)
        self.properties = properties

    def __call__(self, left, right):
        return self.call(left, right)


AddProperties = BinProperties(True, True, {'*': True}, {'*': True})
Add = BinOperator('+', 1, AddProperties, lambda x, y: x + y)


MulProperties = BinProperties(True, True, {'+': True}, {'+': True})
Mul = BinOperator('*', 2, MulProperties, lambda x, y: x * y)

Neg = UnaryOperator('-', -1, lambda x: -x)
Parenthesis = UnaryOperator('()', 0, lambda x: x)

