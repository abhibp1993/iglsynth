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

        - Vertex has a name.
        - When game is constructed from transition system and an automaton
            the vertex stores tsys and aut vertices.
        - Vertex inherits properties of TSys.Vertex and Automaton.Vertex by
            overriding __setattr__ and __getattr__ methods.

        .. fixme: How to resolve repeated properties of TSys.Vertex and Automaton.Vertex?
        """

        def __init__(self, name, tsys_v=None, aut_v=None):
            assert issubclass(tsys_v, TSys.Vertex) or tsys_v is None
            assert issubclass(aut_v, Automaton.Vertex) or aut_v is None

            self._name = name
            self._tsys_v = tsys_v
            self._aut_v = aut_v

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

    class Edge(Graph.Edge):
        """
        Represents an action-labeled edge of game.

        - :class:`Edge` represents a directed edge labeled with an action.
        - Two edges are equal if they share equal source and target vertices
            and have identical action labels.

        :param u: (:class:`Vertex`) Source vertex of edge.
        :param v: (:class:`Vertex`) Target vertex of edge.
        :param act: (pyobject) An action label of edge. (Default: None)
        """
        def __init__(self, u: 'Game.Vertex', v: 'Game.Vertex', act=None):
            super(Graph.Edge, self).__init__(u=u, v=v)
            self._act = act

        def __eq__(self, other):
            return self.source == other.source and self.target == other.target and self.action == other.action

        def __hash__(self):
            return (self.source, self.target, self.action).__hash__()

        @property
        def action(self):
            return self._act

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, kind, vtype=None, etype=None, graph=None, file=None):
        assert kind in [TURN_BASED, CONCURRENT]
        super(Game, self).__init__(vtype, etype, graph, file)
        self._kind = kind

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def kind(self):
        return self._kind

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def _define_by_graph(self, graph):
        raise NotImplementedError("***********DO NOT IMPLEMENT THIS**************")

    def _define_by_tsys_aut(self, tsys, aut):
        # TODO: Implement this one!
        pass

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def define(self, graph=None, tsys=None, aut=None):
        if graph is not None and tsys is None and aut is None:
            self._define_by_graph(graph)

        elif graph is None and tsys is not None and aut is not None:
            self._define_by_tsys_aut(tsys, aut)

        else:
            AttributeError("Either provide a graph or (tsys and aut) parameter, but not both.")