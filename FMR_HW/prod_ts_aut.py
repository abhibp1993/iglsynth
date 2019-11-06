"""
HW Problem 2 for Formal Methods in Robotics.
    Implement the `product` function for constructing the graph of
    product of a transition system with automaton (in this exercise,
    a DFA).

Instructor: Jie Fu
Author: Abhishek N. Kulkarni
"""

from iglsynth.game.gridworld import *
from iglsynth.logic.ltl import *


class Game(Graph):
    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    class Vertex(Graph.Vertex):
        """
        Represents a vertex in game.

        - Vertex has a name.
        - When game is constructed from transition system and an automaton
            the vertex stores tsys and aut vertices.
        - Vertex inherits properties of TSys.Vertex and Automaton.Vertex by
            overriding __setattr__ and __getattr__ methods.

        .. fixme: How to resolve repeated properties of TSys.Vertex and Automaton.Vertex?
        """

        def __init__(self, name, tsys_v=None, aut_v=None):
            assert issubclass(tsys_v.__class__, TSys.Vertex) or tsys_v is None
            assert issubclass(aut_v.__class__, Automaton.Vertex) or aut_v is None

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
            super(Game.Edge, self).__init__(u=u, v=v)
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


def test_ts_aut_product():

    # 1. Define atomic propositions
    #   TODO: Change the implementation of AP's based on your LTL formula.
    a = AP("a", lambda st, *args, **kwargs: True)
    b = AP("b", lambda st, *args, **kwargs: False)

    sigma = Alphabet([a, b])

    # 2. Define a transition system.
    #   (Hint: You may want to use Gridworld from gw_graph.)
    tsys = TSys(kind=TURN_BASED, props=sigma)

    # 3. Define an automaton object.
    #   Use spot to get automaton for some COSAFE specification,
    #   e.g. phi = F(a & Fb)
    #
    # REMARK. Automaton.translate() function is broken. DO NOT USE IT.
    aut = Automaton(acc_cond=Automaton.ACC_COSAFE)

    # Create a game.
    game = Game(kind=TURN_BASED)
    game.define(tsys=tsys, aut=aut)

    # Write assert statements that test whether the construction is correct or not.
    assert game.num_vertices == 0           # TODO: Change the number, by theoretically calculation
    assert game.num_edges == 0              # TODO: Change the number, by theoretically calculation


if __name__ == '__main__':
    test_ts_aut_product()
