from python_symb.Expressions.expr import Expr
from python_symb.MathTypes.symbols import Var
from python_symb.MathTypes.operator_file import Operator, BinOperator, Add, Mul

def expand(expr: Expr) -> Expr:
    """
    Expand an expression
    :param expr: expression to expand
    :return: expanded expression
    """

    if expr.is_leaf:
        return expr

