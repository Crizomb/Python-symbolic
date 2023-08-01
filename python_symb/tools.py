from __future__ import annotations
from typing import *


def gcd(a, b):

    if b > a:
        return gcd(b, a)

    if b == 0:
        return a

    return gcd(b, a % b)

