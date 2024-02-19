from __future__ import annotations
from typing import *


def gcd(a, b):
    """
    Greatest common divisor
    work with any object that support modulo and comparison (contrary to math.gcd)

    used in type : Fraction
    """

    if b > a:
        return gcd(b, a)

    if b == 0:
        return a

    return gcd(b, a % b)

