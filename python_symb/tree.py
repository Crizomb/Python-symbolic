from __future__ import annotations
from typing import Iterable, Generator
from collections import deque


class Tree:
    """
    Ultra generic Test class. Can be used to represent any Test structure.

    value : value of the node. Can be a binary operator like "+", a ternary operator like "if", a number etc...

    depth_first_order : the default order of the node in the depth first traversal. Used to implement the depth_first method.
    0 is pre-order, 1 is in-order (for binary Test), -1 is post-order.
    for instance to write "a ? b : c" you need to write Tree("?", [Tree("a"), Tree("b"), Tree("c")])
    and set the depth_first_order of the "?" node to 1.

    children : the children of the node. Can be empty.
    """
    __slots__ = ['value', 'children', 'depth_first_order']

    def __init__(self, value, children: Iterable[Tree] = None, depth_first_order: int = 0):
        self.value = value
        self.depth_first_order = depth_first_order
        self.children = children if children else []

    def __repr__(self) -> str:
        return f'Tree({self.value}, {self.children})'

    def height(self) -> int:
        return 1 + max((child.height() for child in self.children), default=0)

    def size(self) -> int:
        return 1 + sum(child.size() for child in self.children)

    def breadth_first(self) -> Generator[Tree]:

        queue = deque([self])

        while queue:
            poped = queue.popleft()
            for child in poped.children:
                queue.append(child)

            yield poped

    def depth_first_default(self) -> Generator[Tree]:

        def aux(tree):
            n = len(tree.children)
            if not tree.children:
                yield tree

            for i, child in enumerate(tree.children):
                if i == tree.depth_first_order:
                    yield tree

                yield from aux(child)

            if tree.depth_first_order == -1:
                yield tree

        yield from aux(self)

    def depth_first_pre_order(self) -> Generator[Tree]:

        def aux(tree):
            yield tree
            for child in tree.children:
                yield from aux(child)

        yield from aux(self)

    def depth_first_post_order(self) -> Generator[Tree]:

        def aux(tree):
            for child in tree.children:
                yield from aux(child)
            yield tree

        yield from aux(self)