"""
iglsynth: core.py

License goes here...
"""

from inspect import signature
from typing import Callable

CONCURRENT = "Concurrent"
TURN_BASED = "Turn-based"


class Player(object):
    pass


class Action(object):
    def __init__(self, name=None, func=None):
        assert isinstance(func, Callable), f"Input parameter func must be a function, got {func.__class__}."
        assert len(signature(func).parameters) == 1, f"Function 'func' must take exactly one parameter."

        self._name = name
        self._func = func

    def __repr__(self):
        return f"Action(name={self._name})"

    def __call__(self, v):
        return self._func(v)


def action(func):
    """
    Decorator for creating atomic propositions.
    """
    a = Action(name=func.__name__, func=func)
    return a

