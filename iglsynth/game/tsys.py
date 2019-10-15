from iglsynth.game.kripke import *
from iglsynth.game.arena import *
from iglsynth.game.bases import Player

TURN_BASED = "Turn-based"
CONCURRENT = "Concurrent"


class TSys(Kripke):

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    class Edge(Graph.Edge):
        """
        Class for representing a action-labeled edge of graph.

        - :class:`Edge` represents a directed, and action-labeled edge.
        - Two edges are equal, if the both have equal source vertices <AND>
            equal target vertices <AND> equal actions.

        :param u: (:class:`Vertex`) Source vertex of edge.
        :param v: (:class:`Vertex`) Target vertex of edge.
        :param act: (Hashable object) Action label of edge.
        """
        ACTIONS = set()

        def __hash__(self):
            return (self._source, self._target).__hash__()

        def __init__(self, u: 'TSys.Vertex', v: 'TSys.Vertex', act):
            super(TSys.Edge, self).__init__(u=u, v=v)
            self._act = act
            TSys.Edge.ACTIONS.add(act)

        def __repr__(self):
            return f"Edge(source={self._source}, target={self._target}, act={self._act})"

        def __eq__(self, other: 'TSys.Edge'):
            return self.source == other.source and self.target == other.target and self.act == other.act

        @property
        def act(self):
            return self._act

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, kind, arena=None, p1=None, p2=None,
                 actions=None, props=None, label_func=None,
                 vtype=None, etype=None, graph=None, file=None):

        # Default values
        vtype = TSys.Vertex if vtype is None else vtype
        etype = TSys.Edge if etype is None else etype
        actions = set() if actions is None else actions
        props = set() if props is None else props

        # Validate input arguments
        assert kind in [TURN_BASED, CONCURRENT], f"A TSys kind must be either {TURN_BASED} or {CONCURRENT}."

        assert isinstance(arena, Arena) or arena is None
        assert isinstance(p1, Player) or p1 is None
        assert isinstance(p2, Player) or p2 is None
        assert isinstance(actions, Iterable)

        assert issubclass(vtype, TSys.Vertex), "vtype must be a sub-class of TSys.Vertex."
        assert issubclass(etype, TSys.Edge), "etype must be a sub-class of TSys.Edge."

        assert all([isinstance(p, AP) for p in props])
        assert isinstance(label_func, Callable) or label_func is None   # TODO: Change this to signature validation.

        # Base class constructor
        super(TSys, self).__init__(props=props, label_func=label_func, vtype=vtype, etype=etype, graph=graph, file=file)

        # Defining parameters
        self._arena = arena
        self._p1 = p1
        self._p2 = p2
        self._actions = actions
        self._kind = kind

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def arena(self):
        return self._arena

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2

    @property
    def actions(self):
        return TSys.Edge.ACTIONS

    @property
    def kind(self):
        return self._kind

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def initialize(self, init_st: 'TSys.Vertex'):
        assert isinstance(init_st, TSys.Vertex)
        super(TSys, self).initialize(init_st)

    def product_turn_based(self):
        raise NotImplementedError

    def product_concurrent(self):
        raise NotImplementedError
