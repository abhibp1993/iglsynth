"""
iglsynth: game.py

License goes here...
"""


from iglsynth.game.tsys import *
from iglsynth.logic.core import *


class Game(Graph):
    """
    Represents a two-player deterministic **zero-sum** game.

        * The game could be concurrent or turn-based.
        * Game instance can be constructed by adding vertices and edges (See :ref:`Example Game Graph Construction`).

    :param kind: (:data:`CONCURRENT <iglsynth.game.core.CONCURRENT>`
        or :data:`TURN_BASED <iglsynth.game.core.TURN_BASED>`) Whether the game is concurrent or turn-based.
    :param vtype: (:class:`Game.Vertex` or sub-class) The vertex type used to define the game instance.
    :param etype: (:class:`Game.Edge` or sub-class) The edge type used to define the game instance.
    :param graph: (:class:`Game`) A game instance from which "self" instance should be created.
    :param file: (str) An absolute path of file from which the game should be loaded.

    """

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    class Vertex(Graph.Vertex):
        """
        Represents a vertex in game.

        A game vertex is a 3-tuple, ``(name, tsys.v, aut.v)``. When game is
        defined using a graph, `tsys.v` and `aut.v` are both set to None.

        - Vertex must have a name.
        - When game is constructed from transition system and an automaton the vertex stores tsys and aut vertices.

        :param name: (str) The name of the vertex.
        :param turn: (int) The id of player who will make the move at this state.
        :param tsys_v: (:class:`iglsynth.game.tsys.TSys.Vertex`) Vertex of transition system.
        :param aut_v: (:class:`iglsynth.logic.core.Automaton.Vertex`) Vertex of automaton.

        .. note:: When game is defined using transition system and automaton, it is conventional to name vertices
            as ``(tsys_v.name, aut_v.name)``.

        """

        # ------------------------------------------------------------------------------------------------------------------
        # INTERNAL CLASSES
        # ------------------------------------------------------------------------------------------------------------------
        def __init__(self, name, turn=None, tsys_v=None, aut_v=None):
            assert isinstance(tsys_v, TSys.Vertex) or tsys_v is None          
            assert isinstance(aut_v, Automaton.Vertex) or aut_v is None
            assert isinstance(turn, int) or turn is None

            self._name = name
            self._tsys_v = tsys_v
            self._aut_v = aut_v
            self._turn = turn

        def __repr__(self):
            string = f"Vertex(name={self._name}"
            if self._tsys_v is not None:
                string += f", TSys.V={self._tsys_v}"        # pragma: no cover
            if self._aut_v is not None:
                string += f", Aut.V={self._aut_v}"          # pragma: no cover
            string += ")"
            return string

        def __hash__(self):
            return self.name.__hash__()

        def __eq__(self, other):
            return self._name == other._name and self._turn == other._turn

        # ------------------------------------------------------------------------------------------------------------------
        # PUBLIC PROPERTIES
        # ------------------------------------------------------------------------------------------------------------------
        @property
        def name(self):
            """ Returns the name of game vertex. """
            return self._name

        @property
        def turn(self):
            """ Returns the id of player who will make move in current state. """
            return self._turn

        @property
        def tsys_vertex(self):
            return self._tsys_v         # pragma: no cover

        @property
        def aut_vertex(self):
            return self._aut_v          # pragma: no cover

    class Edge(Graph.Edge):
        """
        Represents an action-labeled edge of a game.

        - :class:`Edge <iglsynth.game.game.Game.Edge>` represents a directed edge labeled with an action.
        - Two edges are equal if they share equal source and target vertices
          and have identical action labels.

        :param u: (:class:`Vertex`) Source vertex of edge.
        :param v: (:class:`Vertex`) Target vertex of edge.
        :param act: (:class:`Action <iglsynth.game.core.Action>` or None) An action label of edge. (Default: None)

        .. note:: We have following cases depending on whether game is turn-based or concurrent.

            * (Turn-based) Action must be an :class:`Action <iglsynth.game.core.Action>` object.
            * (Concurrent) Action must be a 2-tuple of (:class:`Action <iglsynth.game.core.Action>`,
              :class:`Action <iglsynth.game.core.Action>`)
        """
        def __init__(self, u: 'Game.Vertex', v: 'Game.Vertex', act=None):
            # Validate type of action
            if isinstance(act, Action):
                pass

            elif isinstance(act, (tuple, list)):
                assert len(act) == 2
                assert isinstance(act[0], Action)
                assert isinstance(act[1], Action)
                act = tuple(act)

            elif act is None:
                pass

            else:
                raise AssertionError(f"Input parameter act must be an Action or a 2-tuple (Action, Action) or None.")

            super(Game.Edge, self).__init__(u=u, v=v)
            self._act = act

        def __eq__(self, other):
            return self.source == other.source and self.target == other.target and self.act == other.act

        def __hash__(self):
            return (self.source, self.target, self.act).__hash__()

        @property
        def act(self):
            return self._act

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, kind, vtype=None, etype=None, graph=None, file=None):

        assert kind in [TURN_BASED, CONCURRENT], \
                f"Parameter 'kind' must be either TURN_BASED or CONCURRENT. Got {kind}."

        # Initialize internal variables
        self._kind = kind
        self._p1_spec = None
        super(Game, self).__init__(vtype, etype, graph, file)

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def kind(self):
        """
        Returns the kind of game, whether :data:`TURN_BASED <iglsynth.game.core.TURN_BASED>` or
        :data:`CONCURRENT <iglsynth.game.core.CONCURRENT>`.
        """
        return self._kind

    @property
    def p1_spec(self):
        return self._p1_spec

    # ------------------------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def _product_turn_based_tsys_aut(self, tsys, aut):
        # TODO: Implement this one!
        pass        # pragma: no cover

    def _product_concurrent_tsys_aut(self, tsys, aut):
        # TODO: Implement this one!
        pass        # pragma: no cover

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def add_vertex(self, v: 'Game.Vertex'):
        if self._kind == TURN_BASED:
            assert v.turn is not None
        else:   # kind is CONCURRENT
            assert v.turn is None

        super(Game, self).add_vertex(v)

    def add_edge(self, e: 'Game.Edge'):

        if self._kind == TURN_BASED:
            assert isinstance(e.act, Action) or e.act is None
        else:   # kind is CONCURRENT
            act = e.act
            if act is not None:
                assert isinstance(act, (list, tuple))
                assert len(act) == 2
                assert isinstance(act[0], Action)
                assert isinstance(act[1], Action)
        
        super(Game, self).add_edge(e)

    def define(self, tsys=None, p1_spec=None):      # pragma: no cover
        """
        Defines and constructs the deterministic zero-sum game graph.

        :param tsys: (:class:`TSys`) Transition system over which game is defined.
        :param p1_spec: (:class:`ILogic`) Logical specification that P1 must satisfy over transition system.

        .. note:: A game graph can be defined in three possible ways.

            * Explicit construction of graph by adding vertices and edges.
            * By providing transition system and a logical specification for P1.
            * By providing an game field and two players. (Not presently supported).

        """
        # If transition system and specification are provided, then construct game using appropriate product operation
        if tsys is not None and p1_spec is not None:

            # Validate input arguments
            assert isinstance(p1_spec, ILogic), \
                f"Input argument p1_spec must be an ILogic formula. Received p1_spec={p1_spec}."
            assert isinstance(tsys, TSys), \
                f"Input argument tsys must be an TSys object. Received p1_spec={tsys}."
            assert tsys.kind == self.kind, \
                f"Type of argument tsys={tsys} is {tsys.kind} does NOT match self.kind={self.kind}."

            # Update internal variables
            self._p1_spec = p1_spec

            # Translate the specification to an automaton
            aut = p1_spec.translate()

            # Invoke appropriate product operation
            if self.kind == TURN_BASED:
                self._product_turn_based_tsys_aut(tsys, aut)

            else:
                self._product_concurrent_tsys_aut(tsys, aut)

        else:
            AttributeError("Either provide a graph or (tsys and aut) parameter, but not both.")