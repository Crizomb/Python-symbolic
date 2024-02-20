from __future__ import annotations


class Symbols:
    """
    All maths things (other than integers) that will be parsed need to be of "Symbols" class
    """
    instances = {}

    def __init__(self, name):
        assert name not in Symbols.instances, f'Symbol with name {name} already exists'
        self.name = name
        Symbols.instances[name] = self

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __add__(self, other):
        from python_symb.Expressions.expr import Expr
        return Expr('+', [self, other])

    def __radd__(self, other):
        from python_symb.Expressions.expr import Expr
        return Expr('+', [other, self])

    def __mul__(self, other):
        from python_symb.Expressions.expr import Expr
        return Expr('*', [self, other])

    def __rmul__(self, other):
        from python_symb.Expressions.expr import Expr
        return Expr('*', [other, self])


class Var(Symbols):
    """
    variable, like 'x' in x+2
    """
    instances = {}

    def __init__(self, name):
        super().__init__(name)
        self.__class__.instances[name] = self


