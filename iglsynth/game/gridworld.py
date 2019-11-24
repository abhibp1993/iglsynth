import itertools
from iglsynth.game.core import *
from iglsynth.game.tsys import *


class Gridworld(TSys):
    """
    A graph representing a 2D Gridworld Transition System (TS).
    A Gridworld is a TS where all edges are labeled with actions.

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
    class Vertex(TSys.Vertex):
        """
        Represents a vertex in grid world. A vertex of gridworld is of type,
        .. centered:: ``(name=(p1.x, p1.y, p2.x, p2.y), turn=1/2/None``

        :param coordinate: (4-tuple) A 4-tuple of (p1.x, p1.y, p2.x, p2.y) representing coordinates of P1 and P2.
        :param turn: (int or None) If representing a :data:`TURN_BASED` gridworld, then an integer representing
            P1 (1) or P2 (2). If representing a :data:`CONCURRENT` gridworld, then None.
        """

        # --------------------------------------------------------------------------------------------------------------
        # INTERNAL FUNCTIONS
        # --------------------------------------------------------------------------------------------------------------
        def __init__(self, coordinate, turn):
            assert isinstance(coordinate, (tuple, list)), \
                f"Parameter coordinate must be a 4-tuple of (p1.x, p1.y, p2.x, p2.y). Received {coordinate}."
            assert len(coordinate) == 4

            self._coordinate = coordinate
            super(Gridworld.Vertex, self).__init__(name=str(coordinate), turn=turn)

        def __hash__(self):
            return (self._coordinate, self._turn).__hash__()

        def __eq__(self, other):
            assert type(other) == self.__class__
            return self.coordinate == other.coordinate and self.turn == other.turn

        # --------------------------------------------------------------------------------------------------------------
        # PUBLIC PROPERTIES
        # --------------------------------------------------------------------------------------------------------------
        @property
        def coordinate(self):
            """ Returns joint-coordinates of P1 and P2 as 4-tuple. """
            return self._coordinate

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, dim, kind, alphabet=None, p1_actions=tuple(), p2_actions=tuple(),
                 vtype=None, etype=None, graph=None, file=None):

        # Validate input parameters not validated in super-class constructor
        assert isinstance(dim, (list, tuple)), \
            f"Parameter dim must be an 2-tuple or 2-list. Received {dim.__class__.__name__} instead."
        assert isinstance(dim[0], int) and isinstance(dim[1], int) and len(dim) == 2
        assert dim[0] > 0 and dim[1] > 0, f"Parameter dim must be a 2-tuple of positive integers. Received dim={dim}."

        # Define internal variables
        self._dim = dim

        # Super class cosntructor
        super(Gridworld, self).__init__(kind=kind, alphabet=alphabet, p1_actions=p1_actions, p2_actions=p2_actions,
                                        vtype=vtype, etype=etype, graph=graph, file=file)

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def dim(self):
        """ Returns the dimension of gridworld. """
        return self._dim

    @property
    def nrows(self):
        """ Returns the number of rows in gridworld. """
        return self._dim[0]

    @property
    def ncols(self):
        """ Returns the number of columns in gridworld. """
        return self._dim[1]

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def initialize(self, init_st: 'Gridworld.Vertex'):
        assert self.num_vertices > 0, \
            f"The grid world cannot be initialized before its graph is generated. Did you call gw.generate_graph()?"
        super(Gridworld, self).initialize(init_st)

    def generate_graph(self, p1_actions=None, p2_actions=None):
        """
        Generates the graph of gridworld depending on whether transition system is turn-based or concurrent.
        Time-Complexity of algorithm is  :math:`O( (|Act1| + |Act2}) |V| )`.

        :param p1_actions: (set(:class:`Action`)) Action set of player 1.
        :param p2_actions: (set(:class:`Action`)) Action set of player 2.

        .. note:: ``p1_actions`` and ``p2_actions`` will be ignored if they were
            provided during instantiation of gridworld.

        """

        # Select the right set of actions of P1 and P2.
        if self._p1_action_lock is True:
            if p1_actions is not None:
                warnings.warn(f"P1 action set was provided at the instantiation of Gridworld will be used.")

            p1_actions = self.p1_actions

        if self._p2_action_lock is True:
            if p2_actions is not None:
                warnings.warn(f"P2 action set was provided at the instantiation of Gridworld will be used.")

            p2_actions = self.p2_actions

        # Define a placeholder for actions (This is useful while iterating over actions in turn-based edge construction)
        actions = [p1_actions, p2_actions]

        # Validate actions
        assert all(type(act) == Action for act in p1_actions), f"All actions must be instance of Action class."
        assert all(type(act) == Action for act in p2_actions), f"All actions must be instance of Action class."

        # Construct state space of transition system
        nrows = self.nrows
        ncols = self.ncols
        turn = [1, 2]

        if self.kind == CONCURRENT:
            coordinates = itertools.product(range(nrows), range(ncols), range(nrows), range(ncols))
            vbunch = [self.Vertex(coordinate=point, turn=None) for point in coordinates]
        else:
            coordinates = itertools.product(range(nrows), range(ncols), range(nrows), range(ncols), turn)
            vbunch = [self.Vertex(coordinate=point[0:4], turn=point[4]) for point in coordinates]

        self.add_vertices(vbunch)

        # Construct edges of transition system
        for u in self.vertices:

            # If gridworld is turn-based
            if self.kind == TURN_BASED:
                for act in actions[u.turn - 1]:
                    v = act(u, turn=u.turn)
                    if v in self.vertices:
                        self.add_edge(self.etype(u, v, act))

            # Else, gridworld is concurrent
            else:
                for act1, act2 in itertools.product(p1_actions, p2_actions):
                    v = act1(u, turn=1)
                    v = act2(v, turn=2)
                    if v in self.vertices:
                        e = self.etype(u=u, v=v, action=(act1, act2))
                        self.add_edge(e)


@action
def N(u, **kwargs):
    turn = kwargs["turn"] if u.turn is None else u.turn
    p1x, p1y, p2x, p2y = u.coordinate

    if turn == 1:
        v = u.__class__(coordinate=(p1x, p1y + 1, p2x, p2y), turn=2)

    if turn == 2:
        v = u.__class__(coordinate=(p1x, p1y, p2x, p2y + 1), turn=1)

    if u.turn is None:
        v._turn = None

    return v


@action
def E(u, **kwargs):
    turn = kwargs["turn"] if u.turn is None else u.turn
    p1x, p1y, p2x, p2y = u.coordinate

    if turn == 1:
        v = u.__class__(coordinate=(p1x + 1, p1y, p2x, p2y), turn=2)

    if turn == 2:
        v = u.__class__(coordinate=(p1x, p1y, p2x + 1, p2y), turn=1)

    if u.turn is None:
        v._turn = None

    return v


@action
def S(u, **kwargs):
    turn = kwargs["turn"] if u.turn is None else u.turn
    p1x, p1y, p2x, p2y = u.coordinate

    if turn == 1:
        v = u.__class__(coordinate=(p1x, p1y - 1, p2x, p2y), turn=2)

    if turn == 2:
        v = u.__class__(coordinate=(p1x, p1y, p2x, p2y - 1), turn=1)

    if u.turn is None:
        v._turn = None

    return v


@action
def W(u, **kwargs):
    turn = kwargs["turn"] if u.turn is None else u.turn
    p1x, p1y, p2x, p2y = u.coordinate

    if turn == 1:
        v = u.__class__(coordinate=(p1x - 1, p1y, p2x, p2y), turn=2)

    if turn == 2:
        v = u.__class__(coordinate=(p1x, p1y, p2x - 1, p2y), turn=1)

    if u.turn is None:
        v._turn = None

    return v


CONN_FOUR = [N, E, S, W]
