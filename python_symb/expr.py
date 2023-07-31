from __future__ import annotations
from typing import Union, List, Tuple, Optional, Dict, Callable
from tree import Tree
from operator import Add, Mul, Neg, Parenthesis


class Expr(Tree):

    def __init__(self, value, children=None):
        super().__init__(value, children)



