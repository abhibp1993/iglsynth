from iglsynth.game.kripke import *
from iglsynth.game.arena import *
from iglsynth.game.core import Player, Action

TURN_BASED = "Turn-based"
CONCURRENT = "Concurrent"


class TSys(Kripke):

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    class Vertex(Kripke.Vertex):
        def __init__(self, turn=None):
            assert isinstance(turn, int) or turn is None, \
                f"Parameter 'turn' must be an integer, greater equal 0. Received {turn}."

            self._turn = turn

        @property
        def turn(self):
            return self._turn

    class Edge(Kripke.Edge):
        ACTIONS = set()

        def __init__(self, u, v, act=None):
            super(TSys.Edge, self).__init__(u, v)
            self._act = act
            self.__class__.ACTIONS.add(act)

        def __hash__(self):
            return (self._source, self._target, self._act).__hash__()

        def __repr__(self):
            return f"{self.__class__.__name__}." \
                f"ConcurrentEdge(u={self._source}, v={self._target}, a1={self._act})"

        def __eq__(self, other: 'TSys.Edge'):
            return self._source == other._source and self._target == other._target and self._act == other._act

        @property
        def action(self):
            return self._act

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, kind, field=None, p1=None, p2=None,
                 actions=None, alphabet=None, label_func=None,
                 vtype=None, etype=None, graph=None, file=None):

        # Validate input arguments
        assert kind in [TURN_BASED, CONCURRENT], f"A TSys kind must be either {TURN_BASED} or {CONCURRENT}."
        assert isinstance(field, Field) or field is None
        assert isinstance(p1, Player) or p1 is None
        assert isinstance(p2, Player) or p2 is None
        assert isinstance(actions, Iterable) or actions is None
        assert all([isinstance(p, AP) for p in alphabet]) if alphabet is not None else True
        assert isinstance(label_func, Callable) or label_func is None  # TODO: Change this to signature validation.

        # Set Vertex and Edge type for this object based on kind of transition system
        if kind == TURN_BASED:
            assert issubclass(vtype, TSys.TurnBasedVertex) or vtype is None
            self.Vertex = self.TurnBasedVertex if vtype is None else vtype

            assert issubclass(etype, self.TurnBasedEdge) or etype is None
            self.Edge = self.TurnBasedEdge if etype is None else etype

        else:   # kind == CONCURRENT
            assert isinstance(vtype, TSys.ConcurrentVertex) or vtype is None
            self.Vertex = self.ConcurrentVertex if vtype is None else vtype

            assert isinstance(etype, self.ConcurrentEdge) or etype is None
            self.Edge = self.ConcurrentEdge if etype is None else etype

        # Default values
        vtype = TSys.Vertex if vtype is None else vtype
        etype = TSys.Edge if etype is None else etype
        actions = set() if actions is None else actions
        alphabet = set() if alphabet is None else alphabet

        # Base class constructor
        super(TSys, self).__init__(alphabet=alphabet, label_func=label_func,
                                   vtype=vtype, etype=etype, graph=graph, file=file)

        # Defining parameters
        self._field = field
        self._p1 = p1
        self._p2 = p2
        self._actions = actions
        self._kind = kind

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def field(self):
        return self._field

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2

    @property
    def actions(self):
        return self.Edge.ACTIONS

    @property
    def kind(self):
        return self._kind

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def add_vertex(self, v: 'TSys.Vertex'):
        if self._kind == TURN_BASED:
            assert v.turn is not None
        else:  # kind is CONCURRENT
            assert v.turn is None

        super(TSys, self).add_vertex(v)

    def add_edge(self, e: 'TSys.Edge'):

        if self._kind == TURN_BASED:
            assert isinstance(e.action, Action) or e.action is None
        else:  # kind is CONCURRENT
            act = e.action
            assert len(act) == 2
            assert isinstance(act[0], Action)
            assert isinstance(act[1], Action)

        super(TSys, self).add_edge(e)

    def initialize(self, init_st: 'TSys.Vertex'):
        assert isinstance(init_st, self.Vertex)
        super(TSys, self).initialize(init_st)

    def product_turn_based(self):
        raise NotImplementedError

    def product_concurrent(self):
        raise NotImplementedError
