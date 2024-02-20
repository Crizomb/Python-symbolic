from python_symb.Expressions.expr import Expr
from python_symb.MathTypes.symbols import Var
from python_symb.MathTypes.operator_file import Operator, BinOperator, Add, Mul
from typing import Union


Number = Union[int, float]


def expand(expr: Expr) -> Expr:
    """
    Expand an expression

    :param expr: expression to expand
    :return: expanded expression

    example :
    5*(a+b) -> 5*a + 5*b
    Expr(Mul, [5, Expr(Add, [Expr(a), Expr(b)])]) -> Expr(Add, [Expr(Mul, [5, Expr(a)]), Expr(Mul, [5, Expr(b)])])
    """

    if expr.is_leaf:
        return expr

    match expr:
        case Expr(BinOperator() as Op1, [Expr(Op2, op2_children), right]) if Op2.name in Op1.properties.left_distributive:
            return expand(Expr(Op2, [Expr(Op1, [expand(op2_child), expand(right)]) for op2_child in op2_children]))

        case Expr(BinOperator() as Op1, [left, Expr(Op2, op2_children)]) if Op2.name in Op1.properties.right_distributive:
            return expand(Expr(Op2, [Expr(Op1, [expand(left), expand(op2_child)]) for op2_child in op2_children]))

        case Expr(BinOperator() as Op, [left, right]):
            return Expr(Op, [expand(left), expand(right)])

    return expr


def _regroup(expr: Expr, focus_op: BinOperator) -> Expr:
    """
    regroup an expression, with the contraint that the value of expr is focus_op
    Will be used to regroup an expression

    :param expr: expression to regroup
    :param focus_op: operator to regroup
    :return
    x+x+x+x -> 4*x
    Expr(Add, [Expr(x), Expr(Add, [Expr(x), Expr(Add, [Expr(x), Expr(x)])])]) -> Expr(Mul, [4, Expr(x)])

    with Mul == Add.repeated_op
    """
    assert focus_op.repeated_op is not None, f'{focus_op} has no repeated_op'
    assert expr.value == focus_op, f'{expr.value} is not a {focus_op}'

    # Motifs : Key : (Expr) -> Value : int
    # represent number of times the expression appears in the expression,
    # custom hash make for instance x+y and y+x the same when counting
    motifs = {}

    def collect_motifs(expr: Expr):
        match expr:
            case Expr(BinOperator() as op, [left, right]) if op == focus_op:
                collect_motifs(left)
                collect_motifs(right)
            case Expr(BinOperator() as op, [left, right]) if op == focus_op.repeated_op and isinstance(right.value, Number):
                motifs[left] = motifs.get(expr, 0) + right.value
            case Expr(BinOperator() as op, [left, right]) if op == focus_op.repeated_op and op.properties.commutative and isinstance(left.value, Number):

                motifs[right] = 1 if right not in motifs else motifs[right] + left.value

            case _:
                motifs[expr] = 1 if expr not in motifs else motifs[expr] + 1

    collect_motifs(expr)
    tuple_motifs = list(motifs.items())

    def reconstruct(tuple_motifs):
        match tuple_motifs:
            case [(expr, int(a))]:
                if focus_op.repeated_op.properties.commutative:
                    return Expr(focus_op.repeated_op, [Expr(a), expr])
                return Expr(focus_op.repeated_op, [expr, Expr(a)])
            case [(expr, int(a)), *rest]:
                if focus_op.repeated_op.properties.commutative:
                    return Expr(focus_op, [Expr(focus_op.repeated_op, [Expr(a), expr]), reconstruct(rest)])
                return Expr(focus_op, [Expr(focus_op.repeated_op, [expr, Expr(a)]), reconstruct(rest)])

    return reconstruct(tuple_motifs)

def regroup(expr: Expr, focus_op: BinOperator) -> Expr:
    """
    Regroup an expression

    :param expr: expression to regroup
    :param focus_op: operator to regroup
    :return: regrouped expression

    example :
    x+x+x+x -> 4*x
    Expr(Add, [Expr(x), Expr(Add, [Expr(x), Expr(Add, [Expr(x), Expr(x)])])]) -> Expr(Mul, [4, Expr(x)])
    """

    if expr.is_leaf:
        return expr

    match expr:
        case Expr(BinOperator() as op, [left, right]) if op == focus_op:
            return _regroup(expr, focus_op)

        case Expr(BinOperator() as op, [left, right]):
            return Expr(op, [regroup(left, focus_op), regroup(right, focus_op)])

    return expr


def test():

    x, y = Var('x'), Var('y')
    a, b = Var('a'), Var('b')

    def test_expand():
        expr = (x+y)*(x+y)*(x+y)
        expr = expand(expr)
        expr = regroup(expr, Add)
        print(f"(x+y)*(x+y)*(x+y) -> {expr.to_infix_str()}")
        expr = (x+y+a)*b
        print(f"(x+y+a)*b -> {expand(expr).to_infix_str()}")

    def test_regroup():
        expr = x+2*x+y+y+2*y
        print(f"x+2*x+y+y+2*y -> {regroup(expr, Add).to_infix_str()}")

    def test_power():
        expr = x*x*x + y*y*y
        print(f"x*x*x -> {regroup(expr, Mul).to_infix_str()}")

    def test_all():
        expr = (x+y)*(x+y)*(x+y)
        expanded_expr = expand(expr)
        regrouped_expr = regroup(expanded_expr, Add)
        print(f"(x+y)*(x+y)*(x+y) -> {regrouped_expr.to_infix_str()}")




    test_expand()
    test_regroup()
    test_power()
    #test_all()

if __name__ == "__main__":
    test()


