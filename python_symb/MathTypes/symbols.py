from __future__ import annotations
import traceback



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

    def __add__(self, other) -> Expr:
        from python_symb.Expressions.expr import Expr
        from python_symb.MathTypes.operator_file import Add
        other_expr = other if isinstance(other, Expr) else Expr(other)
        self_expr = Expr(self)
        return Expr(Add, [self_expr, other_expr])

    def __radd__(self, other) -> Expr:
        from python_symb.Expressions.expr import Expr
        from python_symb.MathTypes.operator_file import Add
        other_expr = other if isinstance(other, Expr) else Expr(other)
        self_expr = Expr(self)
        return Expr(Add, [other_expr, self_expr])

    def __mul__(self, other) -> Expr:
        from python_symb.Expressions.expr import Expr
        from python_symb.MathTypes.operator_file import Mul
        other_expr = other if isinstance(other, Expr) else Expr(other)
        self_expr = Expr(self)
        return Expr(Mul, [self_expr, other_expr])

    def __rmul__(self, other) -> Expr:
        from python_symb.Expressions.expr import Expr
        from python_symb.MathTypes.operator_file import Mul
        other_expr = other if isinstance(other, Expr) else Expr(other)
        self_expr = Expr(self)
        return Expr(Mul, [other_expr, self_expr])


class Var(Symbols):
    """
    variable, like 'x' in x+2
    """
    instances = {}

    def __init__(self, name):
        super().__init__(name)
        self.__class__.instances[name] = self

    def to_expr(self):
        from python_symb.Expressions.expr import Expr
        return Expr(self)


def var(name: str) -> Expr:
    """
    Create a variable, return Expr
    """
    from python_symb.Expressions.expr import Expr
    v = Var(name)
    return Expr(v)
