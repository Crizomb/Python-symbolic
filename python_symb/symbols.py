from __future__ import annotations


class Symbols:
    """
    All maths things (other than number) that will be parsed need to be of "Symbols" class
    """
    instances = []

    def __init__(self, name):
        self.name = name
        Symbols.instances.append(self)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Var(Symbols):
    """
    variable, like 'x' in x+2
    """
    instances = []

    def __init__(self, name):
        super().__init__(name)
        print(self.__class__)
        self.__class__.instances.append(self)

