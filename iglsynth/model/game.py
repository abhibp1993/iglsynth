"""
iglsynth: game.py

License goes here...
"""


from iglsynth.model.core import *
import iglsynth.util as util
import iglsynth.model.tsys as tsys
import typing


__all__ = ["Game"]


class GameVertex(util.Vertex):
    def __init__(self, turn=None, data=None, tsys_v=None, aut_v=None):
        # Type checking
        assert isinstance(tsys_v, tsys.TSysVertex)
        # TODO assert isinstance(aut_v, logic.AutomatonVertex)

        # Base class constructor
        super(GameVertex, self).__init__()

        # Update name of vertex to reflect turn
        if tsys_v is None and aut_v is None:
            self._name = (self.id, turn) if data is None else (data, turn)  # Need id to ensure equality is well defined
        elif tsys_v is not None and aut_v is not None:
            self._name = ((self.id, tsys_v, aut_v), turn) if data is None else ((data, tsys_v, aut_v), turn)
        else:
            raise ValueError(f"Both tsys_v and aut_v must either be given or set to None.")

    @property
    def tsys_v(self):
        if isinstance(self._name[0], tuple):
            return self._name[0][1]
        return None

    @property
    def aut_v(self):
        if isinstance(self._name[0], tuple):
            return self._name[0][2]
        return None

    @property
    def data(self):
        if isinstance(self._name[0], tuple):
            return self._name[0][0] if self._name[0][0] != self.id else None
        return None

    @property
    def turn(self):
        return self._name[1]


GameEdge = tsys.TSysEdge


class Game(util.Graph):
    Vertex = GameVertex
    Edge = GameEdge

    def __init__(self, kind, name=None,
                 vertices=None, edges=None,
                 act0=None, act1=None, act2=None, act=None,
                 acc_cond=REACHABILITY):

        # Type checking
        assert kind in [CONCURRENT, TURN_BASED]
        assert acc_cond in ACCEPTANCE_CONDITIONS
        assert all([isinstance(a, (Action, ConcurrentAction)) for a in act0])
        assert all([isinstance(a, (Action, ConcurrentAction)) for a in act1])
        assert all([isinstance(a, (Action, ConcurrentAction)) for a in act2])

        # Base class constructor
        super(Game, self).__init__(name)

        # Add graph properties for transition system
        self._kind = kind
        self._act0 = set(act0) if act0 is not None else None
        self._act1 = set(act1) if act1 is not None else None
        self._act2 = set(act2) if act2 is not None else None
        self._act = set.union(*(s for s in (self._act0, self._act1, self._act2, set(act)) if s is not None))
        self._final = list()
        self._acc_cond = acc_cond
        self._v0 = None

        # Initialize graph with vertices and edges
        if vertices is not None:
            self.add_vertices(vertices)

        if edges is not None:
            self.add_edges(edges)

    @property
    def final(self):
        return self._final

    @final.setter
    def final(self, flist):
        pass

    @property
    def kind(self):
        return self._kind

    def add_vertex(self, v):
        pass

    def add_edge(self, e):
        pass

    def serialize(self, ignores=tuple()):
        pass

    @typing.overload
    def construct(self):
        pass

    def construct(self):
        raise AttributeError("...")


# class Game(Graph):
#     """
#     Represents a two-player deterministic **zero-sum** game.
#
#         * The game could be concurrent or turn-based.
#         * Game instance can be constructed by adding vertices and edges (See :ref:`Example Game Graph Construction`).
#
#     :param kind: (:data:`CONCURRENT <iglsynth.game.core.CONCURRENT>`
#         or :data:`TURN_BASED <iglsynth.game.core.TURN_BASED>`) Whether the game is concurrent or turn-based.
#     :param vtype: (:class:`Game.Vertex` or sub-class) The vertex type used to define the game instance.
#     :param etype: (:class:`Game.Edge` or sub-class) The edge type used to define the game instance.
#     :param graph: (:class:`Game`) A game instance from which "self" instance should be created.
#     :param file: (str) An absolute path of file from which the game should be loaded.
#
#     """
#
   # ------------------------------------------------------------------------------------------------------------------
#     # PRIVATE METHODS
#     # ------------------------------------------------------------------------------------------------------------------
#     def _product_turn_based_tsys_aut(self, tsys, aut):
#         """
#         Computes the product of a turn-based transition system with a specification automaton.
#
#         :param tsys:
#         :param aut:
#         :return:
#         """
#         # Generate vertices of game
#         tsys_states = list(tsys.vertices)
#         aut_states = list(aut.vertices)
#
#         game_states = [self.Vertex(name=f"({s}, {q})", tsys_v=s, aut_v=q, turn=s.turn)
#                        for s in tsys_states for q in aut_states]
#         self.add_vertices(game_states)
#
#         # Set final states
#         for v in self.vertices:
#             if v.aut_vertex in aut.final:
#                 self.mark_final(v)
#
#         # Add edges of game
#         for u in self.vertices:
#             s = u.tsys_vertex
#             q = u.aut_vertex
#
#             s_out_edges = tsys.out_edges(s)
#             q_out_edges = aut.out_edges(q)
#
#             for se in s_out_edges:
#                 for qe in q_out_edges:
#                     # qe_formula = PL(formula=str(qe.formula), alphabet=self.p1_spec.alphabet)
#                     if qe.formula(se.target) is True:
#                         v = self.Vertex(name=f"({se.target}, {qe.target})", tsys_v=se.target,
#                                         aut_v=qe.target, turn=se.target.turn)
#                         self.add_edge(self.Edge(u=u, v=v, act=se.action))
#
#     def _product_concurrent_tsys_aut(self, tsys, aut):
#         # TODO: Implement this one!
#         pass        # pragma: no cover
#
#     # ------------------------------------------------------------------------------------------------------------------
#     # PUBLIC METHODS
#     # ------------------------------------------------------------------------------------------------------------------
#     def add_vertex(self, v: 'Game.Vertex'):
#         if self._kind == TURN_BASED:
#             assert v.turn is not None
#         else:   # kind is CONCURRENT
#             assert v.turn is None
#
#         super(Game, self).add_vertex(v)
#
#     def add_edge(self, e: 'Game.Edge'):
#
#         if self._kind == TURN_BASED:
#             assert isinstance(e.act, Action) or e.act is None
#         else:   # kind is CONCURRENT
#             act = e.act
#             if act is not None:
#                 assert isinstance(act, (list, tuple))
#                 assert len(act) == 2
#                 assert isinstance(act[0], Action)
#                 assert isinstance(act[1], Action)
#
#         super(Game, self).add_edge(e)
#
#     def define(self, tsys=None, p1_spec=None):      # pragma: no cover
#         """
#         Defines and constructs the deterministic zero-sum game graph.
#
#         :param tsys: (:class:`TSys`) Transition system over which game is defined.
#         :param p1_spec: (:class:`ILogic`) Logical specification that P1 must satisfy over transition system.
#
#         .. note:: A game graph can be defined in three possible ways.
#
#             * Explicit construction of graph by adding vertices and edges.
#             * By providing transition system and a logical specification for P1.
#             * By providing an game field and two players. (Not presently supported).
#
#         """
#         # If transition system and specification are provided, then construct game using appropriate product operation
#         if tsys is not None and p1_spec is not None:
#
#             # Validate input arguments
#             assert isinstance(p1_spec, ILogic), \
#                 f"Input argument p1_spec must be an ILogic formula. Received p1_spec={p1_spec}."
#             assert isinstance(tsys, TSys), \
#                 f"Input argument tsys must be an TSys object. Received p1_spec={tsys}."
#             assert tsys.kind == self.kind, \
#                 f"Type of argument tsys={tsys} is {tsys.kind} does NOT match self.kind={self.kind}."
#
#             # Update internal variables
#             self._p1_spec = p1_spec
#
#             # Translate the specification to an automaton
#             aut = p1_spec.translate()
#
#             # Invoke appropriate product operation
#             if self.kind == TURN_BASED:
#                 self._product_turn_based_tsys_aut(tsys, aut)
#
#             else:
#                 self._product_concurrent_tsys_aut(tsys, aut)
#
#         else:
#             AttributeError("Either provide a graph or (tsys and aut) parameter, but not both.")
#
#     def mark_final(self, v):
#         """
#         Adds the given state to the set of final states in the game.
#
#         :param v: (:class:`Game.Vertex`) Vertex to be marked as final.
#         """
#         if v in self.vertices:
#             self._final.add(v)
