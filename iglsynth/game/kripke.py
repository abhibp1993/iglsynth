from typing import Callable
from iglsynth.util.graph import *
# from iglsynth.logic.core import AP


# PATCH - Until logic.AP is defined.
class AP:
    pass


class Kripke(Graph):
    """
    A graph representing a Kripke structure.
    """
    def __init__(self, props=None, label_func=None, vtype=None, etype=None, graph=None, file=None):

        # Validate input data-types
        if vtype is None:
            vtype = Kripke.Vertex
        else:
            assert issubclass(vtype, Kripke.Vertex), "vtype must be a sub-class of Kripke.Vertex."

        if etype is None:
            etype = Kripke.Edge
        else:
            assert issubclass(etype, Kripke.Edge), "etype must be a sub-class of Kripke.Edge."

        # TODO assert all([isinstance(p, AP) for p in props]) or props is None
        assert isinstance(label_func, Callable) or label_func is None   # TODO: Change this to signature validation.

        # Base class constructor
        super(Kripke, self).__init__(vtype=vtype, etype=etype, graph=graph, file=file)

        # Defining parameters
        self._props = props                                                  # Set of atomic propositions
        self._label_fcn = label_func                                         # Labeling function
        self._init_st = None                                                 # Set of initial states

    @property
    def is_left_total(self):
        raise NotImplementedError

    @property
    def props(self):
        return self.props

    def initialize(self, init_st):
        if isinstance(init_st, Iterable):
            assert all(isinstance(st, Kripke.Vertex) for st in init_st)
            self._init_st = set(init_st)

        else:
            assert isinstance(init_st, Kripke.Vertex)
            self._init_st = init_st

    def label(self, v):
        if isinstance(v, self.vtype):
            return self._label_fcn(v)

        elif all(isinstance(u, self.vtype) for u in v):
            return [self._label_fcn(u) for u in v]

        else:
            raise AssertionError(f"Input {v} must be a {self.vtype} object or a bunch of {self.vtype} objects.")
