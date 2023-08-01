from __future__ import annotations
from typing import Dict, Callable
from symbols import Symbols


class Operator(Symbols):
    instances = []
    def __init__(self, name : str, precedence: int, call: Callable):
        super().__init__(name)
        self.precedence = precedence
        self.call = call
        Operator.instances.append(self)

    def __repr__(self):
        return f'{self.name}'


class UnaryOperator(Operator):
    instances = []

    def __init__(self, name: str, precedence: int, call: Callable):
        UnaryOperator.instances.append(self)
        super().__init__(name, precedence, call)

    def __call__(self, expr):
        return self.call(expr)


class BinProperties:

    def __init__(self, associativity: bool, commutativity: True,
                 left_distributivity: Dict[str, bool], right_distributivity: Dict[str, bool]):

        self.associativity = associativity
        self.commutativity = commutativity
        self.left_distributivity = left_distributivity
        self.right_distributivity = right_distributivity


class BinOperator(Operator):
    instances = []

    def __init__(self, name: str, precedence: int, properties: BinProperties, call: Callable):
        BinOperator.instances.append(self)
        super().__init__(name, precedence, call)
        self.properties = properties

    def __call__(self, left, right):
        return self.call(left, right)


AddProperties = BinProperties(True, True, {'*': True}, {'*': True})
Add = BinOperator('+', 2, AddProperties, lambda x, y: x + y)


MulProperties = BinProperties(True, True, {'+': True}, {'+': True})
Mul = BinOperator('*', 3, MulProperties, lambda x, y: x * y)
Sin = UnaryOperator('sin', 0, lambda x: x)

Min = BinOperator('-', 1, AddProperties, lambda x, y: x - y)
# Pns = UnaryOperator('()', 0, lambda x: x)

