from iglsynth.game.tsys import *
from itertools import product


class Gridworld(TSys):
    CONN = {4, 5, 8, 9}
    ACTIONS = {'N', 'E', 'S', 'W', 'NE', 'NW', 'SE', 'SW', 'STAY'}

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    # class Vertex(TSys.Vertex):
    #     """
    #     Represents a vertex in grid world.
    #
    #     - Vertex is of type; (p1.coordinate, p2.coordinate).
    #         User may represent it as a 4-tuple (p1.x, p1.y, p2.x, p2.y) or
    #         a 2-tuple of 2-tuples ((p1.x, p1.y), (p2.x, p2.y)) as per their choice.
    #     -
    #     """
    #     def __init__(self, coord, is_hard_obs=False, is_bouncy_obs=False):
    #         assert isinstance(coord, tuple)
    #         assert isinstance(is_hard_obs, bool) and isinstance(is_bouncy_obs, bool)
    #
    #         self._turn = None               # The variable is private, and should be set within Class Gridworld only.
    #         self._coord = coord
    #         self._is_hard_obs = is_hard_obs
    #         self._is_bouncy_obs = is_bouncy_obs
    #
    #     def __repr__(self):
    #         if self._turn is not None:
    #             return f"Vertex(coord={self._coord}, turn={self._turn})"
    #
    #         return f"Vertex(coord={self._coord})"
    #
    #     def __hash__(self):
    #         return self.coordinate.__hash__()
    #
    #     def __eq__(self, other):
    #         return self.coordinate == other.coordinate
    #
    #     @property
    #     def coordinate(self):
    #         return self._coord
    #
    #     @property
    #     def turn(self):
    #         return self._turn
    #
    #     @turn.setter
    #     def turn(self, val):
    #         assert isinstance(val, int)
    #         assert val > 0
    #         self._turn = val
    #
    #     @property
    #     def is_hard_obs(self):
    #         return self._is_hard_obs
    #
    #     @is_hard_obs.setter
    #     def is_hard_obs(self, val):
    #         assert isinstance(val, bool)
    #         self._is_hard_obs = val
    #
    #     @property
    #     def is_bouncy_obs(self):
    #         return self._is_bouncy_obs
    #
    #     @is_bouncy_obs.setter
    #     def is_bouncy_obs(self, val):
    #         assert isinstance(val, bool)
    #         self._is_bouncy_obs = val
    #
    # class Edge(TSys.Edge):
    #     """
    #     Represents an action-labeled edge of grid world.
    #
    #     - :class:`Edge` represents a directed edge labeled with an action.
    #     - Every edge has an action from set {N, E, S, W, NE, NW, SE, SW, STAY}
    #     - Two edges are equal if they share equal source and target vertices
    #         and have identical action labels.
    #
    #     :param u: (:class:`Vertex`) Source vertex of edge.
    #     :param v: (:class:`Vertex`) Target vertex of edge.
    #     :param act: (:py:attr:`Gridworld.ACTIONS`) An action label of edge.
    #     """
    #     __hash__ = TSys.Edge.__hash__
    #
    #     def __init__(self, u: 'Gridworld.Vertex', v: 'Gridworld.Vertex', act):
    #         assert act in Gridworld.ACTIONS or all(a in Gridworld.ACTIONS for a in act)
    #         super(Gridworld.Edge, self).__init__(u=u, v=v, act=act)

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, kind, dim, conn,
                 field=None, p1=None, p2=None,
                 actions=None, alphabet=None, label_func=None,
                 vtype=None, etype=None, graph=None, file=None):

        super(Gridworld, self).__init__(kind=kind, field=field, p1=p1, p2=p2,
                                        actions=actions, alphabet=alphabet, label_func=label_func,
                                        vtype=vtype, etype=etype, graph=graph, file=file)

        assert isinstance(dim, (list, tuple)), f"dim must be an Iterable. Received {dim.__class__.__name__} instead."
        assert isinstance(dim[0], int) and isinstance(dim[1], int) and len(dim) == 2
        assert conn in Gridworld.CONN

        self._dim = dim
        self._conn = conn

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def dim(self):
        return self._dim

    @property
    def nrows(self):
        return self._dim[0]

    @property
    def ncols(self):
        return self._dim[1]

    @property
    def conn(self):
        return self._conn

    @property
    def hard_obs(self):
        return iter(v for v in self.vertices if v.is_hard_obs)

    @property
    def bouncy_obs(self):
        return iter(v for v in self.vertices if v.is_bouncy_obs)

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def initialize(self, init_st: 'Gridworld.Vertex'):
        assert self.num_vertices > 0 and self.num_edges > 0, \
            f"The grid world cannot be initialized before its graph is generated. Did you call gw.generate_graph()?"
        super(Gridworld, self).initialize(init_st)

    def generate_graph(self):
        raise NotImplementedError



