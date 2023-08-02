from __future__ import annotations
from typing import Iterable, Generator
from tools import gcd


class Fraction:
    """
    Should represent a fraction not a division
    """
    __slots__ = ['num', 'den']
    __match_args__ = ("num", "den")

    #todo check if num and den are part of a domain, so a/b as a meaning a gcd work well
    #todo implement __iadd__ etc... if performance needed

    def __init__(self, *args):
        match args:
            case num, den:
                self.num = num
                self.den = den
            case x, :
                self.num = x
                self.den = 1

    def __repr__(self):
        return f'Fractions({self.num}, {self.den})'

    def simplify_gcd(self):
        """Simplify fraction by diving num and den by their gcd
        return None"""
        match self.num, self.den:
            case int(num), int(den):
                gcd_ = gcd(num, den)
                self.num //= gcd_
                self.den //= gcd_
            # can be completed with others objects that support gcd like polynomials etc...

    def simplify_to_num(self):
        """from frac(a, 1) return a."""
        if self.den == 1:
            return self.num
    def simplify_nested(self, rec=True):
        """simplify nested fractions.
        Fractions(1, Fractions(1, Fractions(1, Fractions(1, 2)))) -> Fractions(2, 1)
        For one simplification step put rec=False

        return None"""

        def aux(fract):
            match fract:
                case Fraction(Fraction(a, b), Fraction(c, d)):
                    fract.num = a * d
                    fract.den = b * c
                case Fraction(num, Fraction(a, b)):
                    fract.num = num * b
                    fract.den = a
                case Fraction(Fraction(a, b), den):
                    fract.num = a
                    fract.den = b * den
            
            if rec:
                num, den = self.num, self.den
                if isinstance(num, Fraction) or isinstance(den, Fraction):
                    aux(fract)

        aux(self)

    def simplify_all_(self):
        self.simplify_gcd()
        self.simplify_nested()
        res = self.simplify_to_num()
        if res:
            return res

        return self

    def __add__(self, other):
        match other:
            case int(x):
                return Fraction(self.num + self.den * x, self.den)
            case Fraction(num, den):
                result = Fraction(self.num * den + num * self.den, self.den * den)
                return result
        return ValueError

    def __radd__(self, other):
        return other + self

    def __neg__(self):
        return Fraction(-self.num, self.den)

    def __mul__(self, other):
        match other:
            case int(x):
                return Fraction(self.num * x, self.den)
            case Fraction(num, den):
                result = Fraction(self.num * num, self.den * den)
                return result
        return ValueError

    def __rmul__(self, other):
        return self*other

    def __truediv__(self, other):
        match other:
            case int(x):
                return Fraction(self.num, self.den * x)
            case Fraction(num, den):
                return Fraction(self.num * den, self.den * num)

    def __rtruediv__(self, other):
        res = self/other
        return Fraction(res.den, res.num)


if __name__ == "__main__":
    a = Fraction(1, 2)
    a += 1
    print(a)












