import iglsynth.util as util
from iglsynth.model.core import *


class TSysVertex(util.Vertex):
    def __init__(self, name=None, turn=None):
        # Type checking
        assert turn in [None, TURN_ENV, TURN_P1, TURN_P2]

        # Base class constructor
        super(TSysVertex, self).__init__(name)

        # Update name of vertex to reflect turn
        if name is None:
            self._name = (self.id, turn)
        else:
            self._name = (name, turn)

    @property
    def turn(self):
        return self._name[1]


class TSysEdge(util.Edge):
    def __init__(self, u, v, a):
        super(TSysEdge, self).__init__(u=u, v=v, name=(u, v, a))

    @property
    def act(self):
        return self._name[2]


class TSys(util.Graph):
    Vertex = TSysVertex
    Edge = TSysEdge

    def __init__(self, kind, name=None,
                 vertices=None, edges=None,
                 act0=None, act1=None, act2=None, act=None,
                 alphabet=None, label_func=None):

        # Type checking
        assert kind in [CONCURRENT, TURN_BASED], '...'
        assert all([isinstance(a, (Action, ConcurrentAction)) for a in act0]), '...'
        assert all([isinstance(a, (Action, ConcurrentAction)) for a in act1]), '...'
        assert all([isinstance(a, (Action, ConcurrentAction)) for a in act2]), '...'

        # Base class constructor
        super(TSys, self).__init__(name)

        # Add graph properties for transition system
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

    @property
    def prop(self):
        return self._prop

    def add_vertex(self, v):
        if self._kind == CONCURRENT:
            assert v.turn is not None, '...'

        super(TSys, self).add_vertex(v)

    def add_edge(self, e):
        # Check consistency.
        u = e.source
        a = e.act

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

    def trans(self, u, a):
        assert u in self
        return iter(e for e in self.out_edges(u) if e.act == a)

    def label_func(self, u):
        assert isinstance(u, self.Vertex) and u in self
        return {p: p(u) for p in self._prop}

