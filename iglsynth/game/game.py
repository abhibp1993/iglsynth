"""
iglsynth: game.py

License goes here...
"""


from iglsynth.game.tsys import *
from iglsynth.logic.core import *


class Game(Graph):

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    class Vertex(Graph.Vertex):
        """
        Represents a vertex in game.

        A game vertex is a 3-tuple, (name, tsys.v, aut.v). When game is
        defined using a graph, `tsys.v` and `aut.v` are set to None.

        - Vertex has a name. Generally, name is a string "(tsys_v.name, aut_v.name)".
        - When game is constructed from transition system and an automaton
            the vertex stores tsys and aut vertices.
        """

        def __init__(self, name, turn=None, tsys_v=None, aut_v=None):
            assert isinstance(tsys_v, (TSys.TurnBasedVertex, TSys.ConcurrentVertex)) or tsys_v is None
            assert isinstance(aut_v, Automaton.Vertex) or aut_v is None
            assert isinstance(turn, int) or turn is None

            self._name = name
            self._tsys_v = tsys_v
            self._aut_v = aut_v
            self._turn = turn

        def __repr__(self):
            string = f"Vertex(name={self._name}"
            if self._tsys_v is not None:
                string += f", TSys.V={self._tsys_v}"
            if self._aut_v is not None:
                string += f", Aut.V={self._aut_v}"
            string += ")"
            return string

        def __hash__(self):
            return self.name.__hash__()

        def __eq__(self, other):
            return self._name == other._name

        def __getattr__(self, item):
            try:
                return self._tsys_v.__getattr__(item)
            except AttributeError:
                pass

            try:
                return self._aut_v.__getattr__(item)
            except AttributeError:
                pass

            raise AttributeError(f"Attribute {item} is not Game/TSys/Automaton attribute.")

        @property
        def name(self):
            return self._name

        @property
        def turn(self):
            return self._turn

        @turn.setter
        def turn(self, player_id):
            if self._turn is None:
                self._turn = player_id

            warnings.warn(f"Property setter call '{self}.turn = {player_id}' is ignored.")

        @property
        def tsys_vertex(self):
            return self._tsys_v

        @property
        def aut_vertex(self):
            return self._aut_v

    class TurnBasedEdge(Graph.Edge):
        """
        Represents an action-labeled edge of a turn-based game.

        - :class:`Edge` represents a directed edge labeled with an action.
        - Two edges are equal if they share equal source and target vertices
            and have identical action labels.

        :param u: (:class:`Vertex`) Source vertex of edge.
        :param v: (:class:`Vertex`) Target vertex of edge.
        :param act: (pyobject) An action label of edge. (Default: None)
        """
        def __init__(self, u: 'Game.Vertex', v: 'Game.Vertex', act=None):
            super(Game.TurnBasedEdge, self).__init__(u=u, v=v)
            self._act = act

        def __eq__(self, other):
            return self.source == other.source and self.target == other.target and self.action == other.action

        def __hash__(self):
            return (self.source, self.target, self.action).__hash__()

        @property
        def action(self):
            return self._act

    class ConcurrentEdge(Graph.Edge):
        """
        Represents an action-labeled edge of a turn-based game.

        - :class:`Edge` represents a directed edge labeled with an action.
        - Two edges are equal if they share equal source and target vertices
            and have identical action labels.

        :param u: (:class:`Vertex`) Source vertex of edge.
        :param v: (:class:`Vertex`) Target vertex of edge.
        :param act: (pyobject) An action label of edge. (Default: None)
        """

        def __init__(self, u: 'Game.Vertex', v: 'Game.Vertex', act=None):
            assert act is None or (isinstance(act, (list, tuple)) and len(act) == 2), \
                f"Parameter 'act' of ConcurrentEdge must be None or " \
                f"a list/tuple of length of 2 representing (act1, act2)."

            super(Game.ConcurrentEdge, self).__init__(u=u, v=v)
            self._act = act

        def __eq__(self, other):
            return self.source == other.source and self.target == other.target and self.action == other.action

        def __hash__(self):
            return (self.source, self.target, self.action).__hash__()

        @property
        def action(self):
            return self._act

        @property
        def p1_action(self):
            return self._act[0]

        @property
        def p2_action(self):
            return self._act[1]

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, kind, vtype=None, etype=None, graph=None, file=None):

        # Validate type of game
        if kind == TURN_BASED:
            etype = Game.TurnBasedEdge if etype is None else etype

        elif kind == CONCURRENT:
            etype = Game.ConcurrentEdge if etype is None else etype

        else:
            assert kind in [TURN_BASED, CONCURRENT], \
                f"Parameter 'kind' must be either TURN_BASED or CONCURRENT. Got {kind}."

        # Initialize internal variables
        self._kind = kind
        super(Game, self).__init__(vtype, etype, graph, file)

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def kind(self):
        return self._kind

    # ------------------------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------------------------
    # def _define_by_graph(self, graph):
    #     raise NotImplementedError("***********DO NOT IMPLEMENT THIS**************")

    def _define_by_tsys_aut(self, tsys, aut):
        # TODO: Implement this one!
        pass

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def define(self, tsys=None, aut=None):
        if tsys is not None and aut is not None:
            self._define_by_tsys_aut(tsys, aut)

        else:
            AttributeError("Either provide a graph or (tsys and aut) parameter, but not both.")