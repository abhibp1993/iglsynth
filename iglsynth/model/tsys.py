
__all__ = ["TSys"]


import iglsynth.util as util
from iglsynth.model.core import *


class TSysVertex(util.Vertex):
    def __init__(self, state=None, turn=None, **kwargs):
        # If state is provided by user, then we set the name of vertex as state + turn
        if state is not None:
            super(TSysVertex, self).__init__(name=(state, turn), **kwargs)

        # Otherwise, the vertex is identified by the automatically generated name
        else:
            super(TSysVertex, self).__init__(**kwargs)

        # Internal data structure
        self._turn = turn

    @property
    def turn(self):
        return self._turn


class TSysEdge(util.Edge):
    def __init__(self, u, v, a, **kwargs):
        assert isinstance(a, (Action, ConcurrentAction))
        super(TSysEdge, self).__init__(u=u, v=v, name=(u, v, a), **kwargs)
        self._a = a

    @property
    def action(self):
        return self._a


class TSys(util.Graph):
    Vertex = TSysVertex
    Edge = TSysEdge

    def __init__(self, kind=CONCURRENT, name=None,
                 vertices=None, edges=None,
                 act0=None, act1=None, act2=None, act=None,
                 alphabet=None, label_func=None):

        # Type checking
        assert kind in [CONCURRENT, TURN_BASED]
        assert all([isinstance(a, (Action, ConcurrentAction)) for a in act0]) if act0 is not None else True
        assert all([isinstance(a, (Action, ConcurrentAction)) for a in act1]) if act1 is not None else True
        assert all([isinstance(a, (Action, ConcurrentAction)) for a in act2]) if act2 is not None else True
        assert all([isinstance(a, (Action, ConcurrentAction)) for a in act]) if act is not None else True

        # Base class constructor
        super(TSys, self).__init__(name)

        # Add graph properties for transition system
        #   First, preprocess act.
        #   act0, act1, act2 may be None (to represent not-given-by-user)
        #   act must be a (possibly empty) set.
        act = set(act) if act is not None else set()
        self._kind = kind
        self._act0 = set(act0) if act0 is not None else None
        self._act1 = set(act1) if act1 is not None else None
        self._act2 = set(act2) if act2 is not None else None
        self._act = set.union(*(s for s in (self._act0, self._act1, self._act2, set(act)) if s is not None))
        self._prop = alphabet
        self._v0 = None

        if label_func is not None:
            self.label_func = label_func

        # Initialize graph with vertices and edges
        if vertices is not None:
            self.add_vertices(vertices)

        if edges is not None:
            self.add_edges(edges)

    @property
    def states(self):
        return set(self.vertices)

    @property
    def act0(self):
        return self._act0

    @property
    def act1(self):
        return self._act1

    @property
    def act2(self):
        return self._act2

    @property
    def act(self):
        return self._act

    @act.setter
    def act(self, val):
        assert all([isinstance(a, (Action, ConcurrentAction)) for a in val])
        self._act = val

    @property
    def prop(self):
        return self._prop

    def add_vertex(self, v):
        if self._kind == CONCURRENT:
            assert v.turn is None
        else:
            assert v.turn in [TURN_P1, TURN_P2, TURN_ENV]

        super(TSys, self).add_vertex(v)
        # TODO: Label vertex with propositions here itself.

    def add_edge(self, e):
        # Check consistency.
        u = e.source
        a = e.action

        if u.turn is None:
            assert isinstance(a, ConcurrentAction)

        elif u.turn == TURN_ENV:
            assert (a in self._act0) if self._act0 is not None else (a in self._act)

        elif u.turn == TURN_P1:
            assert (a in self._act1) if self._act1 is not None else (a in self._act)

        elif u.turn == TURN_P2:
            assert (a in self._act2) if self._act2 is not None else (a in self._act)

        else:
            raise ValueError(f"")

        super(TSys, self).add_edge(e)

    def initialize(self, v):
        assert v in self, '...'
        self._v0 = v

    def delta(self, u, a):
        assert u in self
        return iter(e for e in self.out_edges(u) if e.action == a)

    def label_func(self, u):
        assert isinstance(u, self.Vertex) and u in self
        return {p: p(u) for p in self._prop}
