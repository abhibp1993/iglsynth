"""
iglsynth: core.py

License goes here...
"""

from inspect import signature
from typing import Callable


# Module level configuration parameters for users
TURN_BASED = "Turn-based"
CONCURRENT = "Concurrent"

TURN_ENV = "TURN_ENV"
TURN_P1 = "TURN_P1"
TURN_P2 = "TURN_P2"

REACHABILITY = "REACHABILITY"
SAFETY = "SAFETY"
ACCEPTANCE_CONDITIONS = [REACHABILITY, SAFETY]

class Player(object):
    pass


class Action(object):
    """
    Represents an action.
    An action acts on a state (of :class:`TSys` or :class:`Game` etc.) to produce a new state.

    :param name: (str) Name of the action.
    :param func: (function) An implementation of action.

    .. note:: Acceptable function templates are,

        * ``st <- func(st)``
        * ``st <- func(st, *args)``
        * ``st <- func(st, **kwargs)``
        * ``st <- func(st, *args, **kwargs)``

    """
    def __init__(self, name=None, func=None):
        assert isinstance(func, Callable), f"Input parameter func must be a function, got {type(func)}."
        assert len(signature(func).parameters) in [1, 2, 3], f"Function 'func' must take exactly one parameter."

        self._name = name
        self._func = func

    def __repr__(self):
        return f"Action(name={self._name})"

    def __call__(self, v, *args, **kwargs):
        return self._func(v, *args, **kwargs)


class ConcurrentAction(object):
    """
    Represents an action.
    An action acts on a state (of :class:`TSys` or :class:`Game` etc.) to produce a new state.

    :param name: (str) Name of the action.
    :param func: (function) An implementation of action.

    .. note:: Acceptable function templates are,

        * ``st <- func(st)``
        * ``st <- func(st, *args)``
        * ``st <- func(st, **kwargs)``
        * ``st <- func(st, *args, **kwargs)``

    """
    def __init__(self, name=None, func=None):
        assert isinstance(func, Callable), f"Input parameter func must be a function, got {type(func)}."
        assert len(signature(func).parameters) in [1, 2, 3], f"Function 'func' must take exactly one parameter."

        self._name = name
        self._func = func

    def __repr__(self):
        return f"Action(name={self._name})"

    def __call__(self, v, *args, **kwargs):
        return self._func(v, *args, **kwargs)


def action(func):
    """
    Decorator definition to create :class:`Action` objects.
    """
    a = Action(name=func.__name__, func=func)
    return a

