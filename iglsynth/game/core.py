"""
iglsynth: core.py

License goes here...
"""

import abc
from iglsynth.util.graph import *


CONCURRENT = "Concurrent"
TURN_BASED = "Turn-based"


class Kripke(abc.ABC):
    pass


class Player(object):
    pass


class Action(object):
    pass
