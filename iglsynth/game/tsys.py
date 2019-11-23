from iglsynth.game.kripke import *
from iglsynth.game.arena import *
from iglsynth.game.core import Player, Action

TURN_BASED = "Turn-based"
CONCURRENT = "Concurrent"


class TSys(Kripke):
    """
    A graph representing a Transition System (TS).
    A TS is a Kripke structure where all edges are labeled with actions.

    :param kind: (:data:`TURN_BASED` or :data:`CONCURRENT`) Whether the transition system is turn-based or concurrent.
    :param alphabet: (:class:`Alphabet`) A set of atomic propositions defined over the Kripke structure.
    :param vtype: (class) Class representing vertex objects.
    :param etype: (class) Class representing edge objects.
    :param graph: (:class:`Graph`) Copy constructor. Copies the input graph into new Kripke object.
    :param file: (str) Name of file (with absolute path) from which to load the Kripke graph.

    .. note:: Kripke structure class is defined as a placeholder. It may be used to define structures like
              :class:`TSys`.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    class Vertex(Kripke.Vertex):
        """
        Class for representing a vertex of a transition system.

        - Vertex has a name, which is a unique id.
        - Optionally, a vertex may have a turn associated with it. When ``turn`` is not ``None``,
          then the vertex represents a TURN-BASED transition system. Otherwise, the vertex
          represents a CONCURRENT transition system.

        """
        # --------------------------------------------------------------------------------------------------------------
        # INTERNAL FUNCTIONS
        # --------------------------------------------------------------------------------------------------------------
        def __init__(self, name, turn=None):
            assert isinstance(name, str), f"Parameter 'name' must be a string. " \
                f"Received name={name} of type(name)={type(name)}."
            assert isinstance(turn, int) or turn is None, \
                f"Parameter 'turn' must be an integer, greater equal 0. Received {turn}."

            self._name = name
            self._turn = turn

        def __hash__(self):
            return self._name.__hash__()

        def __eq__(self, other):
            assert type(other) == self.__class__
            return self._name == other.name

        def __repr__(self):
            return f"{self.__class__.__name__}(name={self.name}, turn={self.turn})"

        # --------------------------------------------------------------------------------------------------------------
        # PUBLIC PROPERTIES
        # --------------------------------------------------------------------------------------------------------------
        @property
        def turn(self):
            """ Returns the player whose turn it is at the vertex. """
            return self._turn

        @property
        def name(self):
            """ Returns the name associated with the vertex. """
            return self._name

    class Edge(Kripke.Edge):
        """
        Class for representing a edge of graph.

        :param u: (:class:`TSys.Vertex`) Source vertex of edge.
        :param v: (:class:`TSys.Vertex`) Target vertex of edge.
        :param action: (:class:`Action` ) Action label of the edge.
        """

        # --------------------------------------------------------------------------------------------------------------
        # INTERNAL FUNCTIONS
        # --------------------------------------------------------------------------------------------------------------
        def __init__(self, u, v, action=None):
            super(TSys.Edge, self).__init__(u, v)
            self._action = action

        def __hash__(self):
            return (self._source, self._target, self._action).__hash__()

        def __repr__(self):
            return f"{self.__class__.__name__}." \
                f"{self.__class__.__name__}(u={self._source}, v={self._target}, a1={self._action})"

        def __eq__(self, other: 'TSys.Edge'):
            assert type(other) == self.__class__
            return self._source == other._source and self._target == other._target and self._action == other._action

        # --------------------------------------------------------------------------------------------------------------
        # PUBLIC PROPERTIES
        # --------------------------------------------------------------------------------------------------------------
        @property
        def action(self):
            """ Returns the action associated with the edge. """
            return self._action

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, kind, alphabet=None, vtype=None, etype=None, graph=None, file=None):

        # Validate input arguments
        assert kind in [TURN_BASED, CONCURRENT], f"A TSys kind must be either {TURN_BASED} or {CONCURRENT}."

        # Base class constructor
        super(TSys, self).__init__(alphabet=alphabet, vtype=vtype, etype=etype, graph=graph, file=file)

        # Defining parameters
        self._kind = kind
        self._p1_actions = set()
        self._p2_actions = set()

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def p1_action(self):
        return self._p1_actions

    @property
    def p2_actions(self):
        return self._p2_actions

    @property
    def actions(self):
        return set.union(self._p1_actions, self._p2_actions)

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
