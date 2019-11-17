"""
iglsynth: graph.py

License goes here...
"""

from iglsynth.util.graph import *


class Arena(Graph):
    """
    Represents a deterministic game arena.

    - Arena graph is a digraph, and not a multi-digraph.
    - :class:`Arena.Edge` is differs from :class:Graph.Edge`.
        Two `Arena.Edge` are equal if `e1.source = e2.source` and `e1.target = e2.target`.

    :param vtype: (class) Class representing vertex objects.
    :param etype: (class) Class representing edge objects.
    :param graph: (:class:`Graph`) Copy constructor. Copies the input graph into new Graph object.
    :param file: (str) Name of file (with absolute path) from which to load the graph.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    class Edge(Graph.Edge):
        """
        Class for representing a edge of graph.

        - :class:`Edge` represents a directed edge.
        - Two edges are equal, if the both have equal source and same target vertices.

        :param u: (:class:`Vertex`) Source vertex of edge.
        :param v: (:class:`Vertex`) Target vertex of edge.
        """

        def __hash__(self):
            return (self._source, self._target).__hash__()

        # def __init__(self, u: 'Graph.Vertex', v: 'Graph.Vertex'):
        #     self._source = u
        #     self._target = v
        #
        # def __repr__(self):
        #     return f"Edge(source={self.source}, target={self.target})"

        def __eq__(self, other):
            return self.source == other.source and self.target == other.target

        # @property
        # def source(self):
        #     """ Returns the source vertex of edge. """
        #     return self._source
        #
        # @property
        # def target(self):
        #     """ Returns the target vertex of edge. """
        #     return self._target

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, vtype=None, etype=None, graph=None, file=None):

        # Validate input data-types
        if vtype is None:
            vtype = Arena.Vertex
        else:
            assert issubclass(vtype, Arena.Vertex), "vtype must be a sub-class of Arena.Vertex."

        if etype is None:
            etype = Arena.Edge
        else:
            assert issubclass(etype, Arena.Edge), "etype must be a sub-class of Arena.Edge."

        # Construct
        super(Arena, self).__init__(vtype=vtype, etype=etype, graph=graph, file=file)



