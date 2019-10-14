"""
iglsynth: graph.py

License goes here...
"""

from typing import Iterable, Iterator, List, Union
from functools import reduce
import warnings


class Graph(object):
    """
    Base class to represent graph-based objects in IGLSynth.

    - :class:`Graph` may represent a Digraph or a Multi-Digraph.
    - :class:`Edge` may represent a self-loop, i.e. `source = target`.
    - :class:`Graph` stores objects of :class:`Graph.Vertex` and :class:`Graph.Edge` classes or
    their sub-classes, which users may define.
    - :class:`Vertex` and :class:`Edge` may have attributes, which represent the vertex
    and edge properties of the graph.

    :param vtype: (class) Class representing vertex objects.
    :param etype: (class) Class representing edge objects.
    :param graph: (:class:`Graph`) Copy constructor. Copies the input graph into new Graph object.
    :param file: (str) Name of file (with absolute path) from which to load the graph.

    .. todo: The copy-constructor and load-from-file functionality.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL PRIVATE CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    class Vertex(object):
        """
        Base class for representing a vertex of graph.

        - :class:`Vertex` constructor takes no arguments.
        - Two vertices are equal, if the two :class:`Vertex` objects are same.
        """
        __hash__ = object.__hash__

    class Edge(object):
        """
        Base class for representing a edge of graph.

        - :class:`Edge` represents a directed edge.
        - Two edges are equal, if the two :class:`Edge` objects are same.

        :param u: (:class:`Vertex`) Source vertex of edge.
        :param v: (:class:`Vertex`) Target vertex of edge.
        """

        __hash__ = object.__hash__

        def __init__(self, u: 'Graph.Vertex', v: 'Graph.Vertex'):
            self._source = u
            self._target = v

        def __repr__(self):
            return f"Edge(source={self.source}, target={self.target})"

        @property
        def source(self):
            """ Returns the source vertex of edge. """
            return self._source

        @property
        def target(self):
            """ Returns the target vertex of edge. """
            return self._target

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, vtype=None, etype=None, graph=None, file=None):

        # Validate input data-types
        if vtype is None:
            vtype = Graph.Vertex
        else:
            assert issubclass(vtype, Graph.Vertex), "vtype must be a sub-class of Graph.Vertex."

        if etype is None:
            etype = Graph.Edge
        else:
            assert issubclass(etype, Graph.Edge), "etype must be a sub-class of Graph.Edge."

        # Define internal data structure
        self.vtype = vtype                                          # Vertex class used in graph
        self.etype = etype                                          # Edge class used in graph
        self._vertex_edge_map = dict()                              # Dict: {vertex: (set(<in-edge>), set(<out-edge>))}
        self._edges = set()                                         # Set of all edges of graph

        # TODO: Initialize graph by provided (optional) inputs
        if graph is not None and file is None:
            self._instantiate_by_graph(graph)

        # TODO: If file argument is given, then load graph from the file.
        elif file is not None and graph is None:
            self._load(filename=file)

        elif file is not None and graph is not None:
            raise ValueError("file and graph parameters should not be provided simultaneously.")

    def __repr__(self):
        return f"Graph(|V|={self.num_vertices} of type={self.vtype}, |E|={self.num_edges} of type={self.etype})"

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vertices(self) -> Iterator:
        """ Returns an iterator over vertices in graph. """
        return iter(self._vertex_edge_map.keys())

    @property
    def edges(self) -> Iterator:
        """ Returns an iterator over edges in graph. """
        return iter(self._edges)

    @property
    def num_vertices(self) -> int:
        """ Returns the number of vertices in graph. """
        return len(self._vertex_edge_map)

    @property
    def num_edges(self) -> int:
        """ Returns the number of edges in graph. """
        return len(self._edges)

    @property
    def vp_names(self) -> List[str]:
        """ Returns the a list of vertex property names in graph. """
        raise NotImplementedError

    @property
    def ep_names(self):
        """ Returns a list of edge property names in graph. """
        raise NotImplementedError

    @property
    def gp_names(self):
        """ Returns a list of graph property names in graph. """
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def add_vertex(self, v: 'Graph.Vertex'):
        """
        Adds a new vertex to graph.
        An attempt to add existing vertex will be ignored, with a warning.

        :param v: (:class:`Vertex`) Vertex to be added to graph.
        """
        assert isinstance(v, Graph.Vertex), \
            f"Vertex {v} must be object of Graph.Vertex or its sub-class. Given, v is {v.__class__.__name__}"

        # If vertex is not already added, then add it.
        if v not in self._vertex_edge_map:
            self._vertex_edge_map[v] = (set(), set())
        else:
            warnings.warn(f"Vertex {v} is already present in graph. Ignoring request to add.")

    def add_vertices(self, vbunch: Iterable['Graph.Vertex']):
        """
        Adds a bunch of vertices to graph.
        An attempt to add existing vertex will be ignored, with a warning.

        :param vbunch: (Iterable over :class:`Vertex`) Vertices to be added to graph.
        """
        for v in vbunch:
            self.add_vertex(v)

    def rm_vertex(self, v: 'Graph.Vertex'):
        """
        Removes a vertex from the graph.
        An attempt to remove a non-existing vertex will be ignored, with a warning.

        :param v: (:class:`Vertex`) Vertex to be removed.
        """
        assert isinstance(v, Graph.Vertex), \
            f"Vertex {v} must be object of Graph.Vertex or its sub-class. Given, v is {v.__class__.__name__}"

        # Remove incoming and outgoing edges from v, and then remove v
        if v in self._vertex_edge_map:
            in_edges, out_edges = self._vertex_edge_map[v]
            self.rm_edges(in_edges)
            self.rm_edges(out_edges)
            self._vertex_edge_map.pop(v)

    def rm_vertices(self, vbunch: Iterable['Graph.Vertex']):
        """
        Removes a bunch of vertices from the graph.
        An attempt to remove a non-existing vertex will be ignored, with a warning.

        :param vbunch: (Iterable over :class:`Vertex`) Vertices to be removed.
        """
        for v in vbunch:
            self.rm_vertex(v)

    def add_edge(self, e: 'Graph.Edge'):
        """
        Adds an edge to the graph.
        Both the vertices must be present in the graph.

        :raises AttributeError: When at least one of the vertex is not in the graph.
        :raises AssertionError: When argument `e` is not an :class:`Edge` object.
        """
        assert isinstance(e, Graph.Edge), \
            f"e must be an object of Graph.Edge class or its sub-class. Got {e.__class__.__name__}"

        if e in self._edges:
            warnings.warn(f"Edge {e} is already present in graph. Ignoring request to add.")
            return None

        u = e.source
        v = e.target

        if u in self._vertex_edge_map and v in self._vertex_edge_map:
            self._vertex_edge_map[u][1].add(u)
            self._vertex_edge_map[v][0].add(v)
            self._edges.add(e)
            return None

        if u not in self._vertex_edge_map and v not in self._vertex_edge_map:
            raise AttributeError(f"Vertices {u} and {v} are not in graph.")

        elif u in self._vertex_edge_map and v not in self._vertex_edge_map:
            raise AttributeError(f"Vertex {v} is not in graph.")

        else:   # v in self._vertex_edge_map:
            raise AttributeError(f"Vertex {u} is not in graph.")

    def add_edges(self, ebunch: Iterable['Graph.Edge']):
        """
        Adds a bunch of edges to the graph.
        Both the vertices of all edges must be present in the graph.

        :raises AttributeError: When at least one of the vertex is not in the graph.
        :raises AssertionError: When argument `e` is not an :class:`Edge` object.
        """
        for e in ebunch:
            self.add_edge(e)

    def rm_edge(self, e: 'Graph.Edge'):
        """
        Removes an existing edge from the graph.

        .. todo: Implement this function.
        """

        # assert isinstance(e, Graph.Edge), \
        #     f"e must be an object of Graph.Edge class or its sub-class. Got {e.__class__.__name__}"
        #
        # if e not in self._edges:
        #     warnings.warn(f"Edge {e} is not present in graph. Ignoring request to remove edge.")
        #     return None
        #
        # u = e.source
        # v = e.target
        #
        # self._vertex_edge_map[u][1].remove(u)
        # self._vertex_edge_map[v][0].remove(v)
        # self._edges.remove(e)
        raise NotImplementedError

    def rm_edges(self, elist: Iterable['Graph.Edge']):
        """
        Removes a bunch of existing edges from the graph.

        .. todo: Implement this function.
        """
        for e in elist:
            self.rm_edge(e)

    def in_edges(self, v: Union['Graph.Vertex', Iterable['Graph.Vertex']]):
        """
        Returns an iterator over incoming edges to given vertex or vertices.
        In case of vertices, the iterator is defined over the union of set of
        incoming edges of individual vertices.

        :param v: (:class:`Vertex`) Vertex of graph.

        :raises AssertionError: When `v` is neither a :class:`Vertex` object
            nor an iterable of :class:`Vertex` objects.
        """
        if isinstance(v, Graph.Vertex):
            return iter(self._vertex_edge_map[v][0])

        elif isinstance(v, Iterable):
            in_edges = (self._vertex_edge_map[u][0] for u in v)
            return iter(reduce(set.union, in_edges))

        raise AssertionError("v must be a single or an iterable of Graph.Vertex (or its sub-class) objects.")

    def out_edges(self, v: Union['Graph.Vertex', Iterable['Graph.Vertex']]):
        """
        Returns an iterator over outgoing edges to given vertex or vertices.
        In case of vertices, the iterator is defined over the union of set of
        incoming edges of individual vertices.

        :param v: (:class:`Vertex`) Vertex of graph.

        :raises AssertionError: When `v` is neither a :class:`Vertex` object
            nor an iterable of :class:`Vertex` objects.
        """
        if isinstance(v, Graph.Vertex):
            return iter(self._vertex_edge_map[v][1])

        elif isinstance(v, Iterable):
            in_edges = (self._vertex_edge_map[u][1] for u in v)
            return iter(reduce(set.union, in_edges))

        raise AssertionError("v must be a single or an iterable of Graph.Vertex (or its sub-class) objects.")

    def in_neighbors(self, v: Union['Graph.Vertex', Iterable['Graph.Vertex']]):
        """
        Returns an iterator over sources of incoming edges to given vertex or vertices.
        In case of vertices, the iterator is defined over the union of set of
        incoming edges of individual vertices.

        :param v: (:class:`Vertex`) Vertex of graph.

        :raises AssertionError: When `v` is neither a :class:`Vertex` object
            nor an iterable of :class:`Vertex` objects.
        """
        if isinstance(v, Graph.Vertex):
            return iter(e.source for e in self._vertex_edge_map[v][0])

        elif isinstance(v, Iterable):
            return iter(e.source for u in v for e in self._vertex_edge_map[u][0])

        raise ValueError("v must be a single or an iterable of Graph.Vertex (or its sub-class) objects.")

    def out_neighbors(self, v: Union['Graph.Vertex', Iterable['Graph.Vertex']]):
        """
        Returns an iterator over targets of incoming edges to given vertex or vertices.
        In case of vertices, the iterator is defined over the union of set of
        incoming edges of individual vertices.

        :param v: (:class:`Vertex`) Vertex of graph.

        :raises AssertionError: When `v` is neither a :class:`Vertex` object
            nor an iterable of :class:`Vertex` objects.
        """
        if isinstance(v, Graph.Vertex):
            return iter(e.target for e in self._vertex_edge_map[v][1])

        elif isinstance(v, Iterable):
            return iter(e.target for u in v for e in self._vertex_edge_map[u][1])

        raise ValueError("v must be a single or an iterable of Graph.Vertex (or its sub-class) objects.")

    def prune(self, v: 'Graph.Vertex'):
        raise NotImplementedError

    def save(self, filename: str = None, ext: str = 'xml'):
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def _load(self, filename: str):
        raise NotImplementedError

    def _instantiate_by_graph(self, graph):
        raise NotImplementedError


class SubGraph(Graph):
    """
        Represents a sub-graph of :class:`Graph` defined using properties ``vfilt`` and/or ``efilt``.

        :param graph: A graph object.
        :type graph: :class:`Graph`

        :param vfilt_name: Name of the boolean vertex property used to define whether a vertex is in sub-graph or not.
        :type vfilt_name: str

        :param efilt_name: Name of the boolean edge property used to define whether an edge is in sub-graph or not.
        :type efilt_name: str
        """

    def __init__(self, graph: Graph, vfilt_name: str = None, efilt_name: str = None):
        raise NotImplementedError


