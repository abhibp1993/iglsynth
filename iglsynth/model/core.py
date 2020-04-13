"""
iglsynth: core.py

License goes here...
"""

from inspect import signature
from typing import Callable
import iglsynth.util as util


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


class Action(util.Entity):
    def __init__(self, func=None, **kwargs):
        if func is None and "name" in kwargs:
            super(Action, self).__init__(**kwargs)
        elif func is None and "name" not in kwargs:
            super(Action, self).__init__(name=None, **kwargs)
        else:   # func is not None
            super(Action, self).__init__(name=func.__name__, **kwargs)

        # Internal data structure
        self._pre = None
        self._act = func
        self._post = None

    def __call__(self, u, *args, **kwargs):
        v = None

        # Evaluate precondition
        eval_pre = False
        if self._pre is None:
            eval_pre = True
        else:
            eval_pre = self._pre(u, *args, **kwargs)

        # Apply action
        if not eval_pre:
            return v

        if self._act is None:
            return v

        v = self._act(u, *args, **kwargs)

        # Evaluate postcondition
        if self._post is None:
            return v

        v = self._post(v, u, *args, **kwargs)
        return v

    def precondition(self, func):
        self._pre = func
        return self

    def postcondition(self, func):
        self._post = func
        return self


if __name__ == '__main__':

    @Action
    def north(state):
        return state + 1

    @north.precondition
    def north(state):
        return True

    print(north(5))
