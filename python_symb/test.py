from python_symb.MathTypes.symbols import var
from python_symb.Expressions.expr import Expr
from python_symb.MathTypes.operator_file import Add, Mul, Exp, Sin
from python_symb.TreeModification.basic_modif import expand, regroup, ungroup
import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def measure_time(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("@timefn: {} took {} seconds.".format(func.__name__, end_time - start_time))
        return result
    return measure_time


# assert equal use none perfect implementation of __eq__ in expr (using weird handmade hash), be careful

def create_var():
    global x, y
    x = var('x')
    y = var('y')


def test_sum(print_result=False):
    expr = x + y
    expr2 = 5 + x
    if print_result:
        print(f"expr1: {expr}")
        print(f"expr2: {expr2}")

    assert expr == Expr(Add, [Expr(x), Expr(y)])
    assert expr2 == Expr(Add, [Expr(5), Expr(x)])


def test_parse(print_result=False):
    str_expr = "5*(x+y) + x*sin(y)"
    expr = Expr.from_infix_str(str_expr)
    if print_result:
        print(f"expr: {expr}")

    assert expr == Expr(Add, [Expr(Mul, [Expr(5), Expr(Add, [Expr(x), Expr(y)])]), Expr(Mul, [Expr(x), Expr(Sin, [Expr(y)])])])


def test_expr_to_str(print_result=False):
    expr = 5*(x+y) + x*Sin(y)
    str_expr = expr.to_infix_str(implicit_mul=True)
    str_expr_no_implicit = expr.to_infix_str(implicit_mul=False)

    if print_result:
        print(f"str_expr: {str_expr}")
        print(f"str_expr_no_implicit: {str_expr_no_implicit}")

    assert str_expr == "5(x+y)+xsin(y)"
    assert str_expr_no_implicit == "5*(x+y)+x*sin(y)"


def test_expand(print_result=False):
    expr = (x+2)*(x+y)
    expanded = expand(expr)
    expanded_str = expanded.to_infix_str()
    if print_result:
        print(f"expanded: {expanded_str}")

    assert expanded_str == "xx+xy+2x+2y"
    assert expanded == Expr(Add, [Expr(Add, [Expr(Mul, [Expr(x), Expr(x)]), Expr(Mul, [Expr(x), Expr(y)])]), Expr(Add, [Expr(Mul, [Expr(2), Expr(x)]), Expr(Mul, [Expr(2), Expr(y)])])])


def test_regroup(print_result=False):
    expr = x+x+2*x+y+x+3*y+x
    regrouped = regroup(expr, Add)
    regrouped_str = regrouped.to_infix_str()
    if print_result:
        print(f"regrouped: {regrouped_str}")

    assert regrouped_str == "6x+4y"
    assert regrouped == Expr(Add, [Expr(Mul, [Expr(6), Expr(x)]), Expr(Mul, [Expr(4), Expr(y)])])


def test_newton_bin(print_result=False):
    expr = (x+y)**4
    ungrouped = ungroup(expr, Exp)
    expanded = expand(ungrouped)
    expand_grouped = regroup(expanded, Add)
    expand_grouped = regroup(expand_grouped, Mul)

    if print_result:
        print("---")
        print("newton binomial test")
        print("---")
        print(f"expr: {expr.to_infix_str()}")
        print(f"ungrouped: {ungrouped.to_infix_str()}")
        print(f"expanded: {expanded.to_infix_str()}")
        print(f"expand_grouped: {expand_grouped.to_infix_str()}")

    assert expand_grouped == Expr(Add, [Expr(Exp, [Expr(x), Expr(4)]),Expr(Add, [Expr(Mul, [Expr(4),Expr(Mul, [Expr(Exp, [Expr(x), Expr(3)]),Expr(y)])]),Expr(Add, [Expr(Mul, [Expr(6),Expr(Mul, [Expr(Exp, [Expr(x), Expr(2)]),Expr(Exp, [Expr(y), Expr(2)])])]),Expr(Add, [Expr(Mul, [Expr(4),Expr(Mul, [Expr(x),Expr(Exp, [Expr(y), Expr(3)])])]),Expr(Exp, [Expr(y), Expr(4)])])])])])

@timeit
def test_big_bin_for_performance(print_result=False):
    expr = (x+y)**11
    print("a")
    ungrouped = ungroup(expr, Exp)
    print("b")
    expanded = expand(ungrouped)
    print("c")
    expand_grouped = regroup(expanded, Add)
    print("d")
    expand_grouped = regroup(expand_grouped, Mul)
    print("e")

    if print_result:
        print("---")
        print("ultra big newton binomial test")
        print("---")
        print(f"expr: {expr.to_infix_str()}")
        print(f"ungrouped: {ungrouped.to_infix_str()}")
        print(f"expanded: {expanded.to_infix_str()}")
        print(f"expand_grouped: {expand_grouped.to_infix_str()}")

if __name__ == '__main__':
    create_var()
    print_r = True
    test_sum(print_result=print_r)
    test_parse(print_result=print_r)
    test_expr_to_str(print_result=print_r)
    test_expand(print_result=print_r)
    test_regroup(print_result=print_r)
    test_newton_bin(print_result=print_r)
    test_big_bin_for_performance(print_result=print_r)
    print("All tests passed")




