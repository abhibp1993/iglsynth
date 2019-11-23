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

    .. note:: (Behavior of ``p1_actions, p2_actions``). In many cases, it is desirable to define a set of ``p1_actions``
              and ``p2_actions``, while in others it is desirable to construct these sets while adding edges.
              The :class:`TSys` implements both approaches. When ``p1_actions, p2_actions`` are provided during
              instantiation, the action sets (which are provided) are locked and cannot be changed during runtime.
              When the parameters are not provided during instantiation, the sets are constructed while adding edges.

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
            return self._name.__hash__() if self.turn is None else (self._name, self._turn).__hash__()

        def __eq__(self, other):
            assert type(other) == self.__class__
            return self.__hash__() == other.__hash__()

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
    def __init__(self, kind, alphabet=None, p1_actions=tuple(), p2_actions=tuple(),
                 vtype=None, etype=None, graph=None, file=None):

        # Validate input arguments
        assert kind in [TURN_BASED, CONCURRENT], f"A TSys kind must be either {TURN_BASED} or {CONCURRENT}."

        # Base class constructor
        super(TSys, self).__init__(alphabet=alphabet, vtype=vtype, etype=etype, graph=graph, file=file)

        # Defining parameters
        self._kind = kind
        self._p1_actions = set(p1_actions)             # Action set of P1. (type: set)
        self._p2_actions = set(p2_actions)             # Action set of P2. (type: set)
        self._p1_action_lock = True if len(p1_actions) > 0 else False
        self._p2_action_lock = True if len(p2_actions) > 0 else False

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def p1_actions(self):
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
            assert v.turn in [1, 2]         # Presently we only support 2 player games. This might be relaxed later.

        else:  # kind is CONCURRENT
            assert v.turn is None

        super(TSys, self).add_vertex(v)

    def add_edge(self, e: 'TSys.Edge'):

        if self._kind == TURN_BASED:
            assert isinstance(e.action, Action) or e.action is None

            # Check whether p1 actions are locked. If yes, assert that e.action is within p1's action set.
            if e.source.turn == 1:
                if self._p1_action_lock is True:
                    assert e.action in self.p1_actions
                else:
                    self._p1_actions.add(e.action)

            # Check whether p2 actions are locked. If yes, assert that e.action is within p2's action set.
            elif e.source.turn == 2:
                if self._p2_action_lock is True:
                    assert e.action in self.p2_actions
                else:
                    self._p2_actions.add(e.action)

        else:  # kind is CONCURRENT
            act = e.action
            assert isinstance(act, (tuple, list))
            assert len(act) == 2
            assert isinstance(act[0], Action)
            assert isinstance(act[1], Action)

            p1_action = act[0]
            p2_action = act[1]

            # Check whether p1 actions are locked. If yes, assert that e.action is within p1's action set.
            if self._p1_action_lock is True:
                assert p1_action in self.p1_actions
            else:
                self._p1_actions.add(p1_action)

            # Check whether p2 actions are locked. If yes, assert that e.action is within p2's action set.
            if self._p2_action_lock is True:
                assert p2_action in self.p2_actions
            else:
                self._p2_actions.add(p2_action)

        super(TSys, self).add_edge(e)

    def initialize(self, init_st: 'TSys.Vertex'):
        assert isinstance(init_st, self.Vertex)
        super(TSys, self).initialize(init_st)

    def product_turn_based(self):
        raise NotImplementedError

    def product_concurrent(self):
        raise NotImplementedError
