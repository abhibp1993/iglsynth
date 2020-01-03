"""
iglsynth: graph.py

License goes here...
"""

from typing import Iterable, Iterator, List, Union
from functools import reduce
from iglsynth.util.graphml import *
import uuid
import warnings


class Graph(object):
    """
    Base class to represent graph-based objects in IGLSynth.

        * :class:`Graph` may represent a Digraph or a Multi-Digraph.
        * :class:`Graph.Edge` may represent a self-loop, i.e. `source = target`.
        * :class:`Graph` stores objects of :class:`Graph.Vertex` and :class:`Graph.Edge` classes or
          their sub-classes, which users may define.
        * :class:`Graph.Vertex` and :class:`Graph.Edge` may have attributes, which represent the vertex
          and edge properties of the graph.

    :param vtype: (class) Class representing vertex objects.
    :param etype: (class) Class representing edge objects.
    :param graph: (:class:`Graph`) Copy constructor. Copies the input graph into new Graph object.
    :param file: (str) Name of file (with absolute path) from which to load the graph.

    .. todo:: The copy-constructor and load-from-file functionality.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    class Vertex(object):
        """
        Base class for representing a vertex of graph.

        :param name: (object) A unique identifier for the vertex.

        - Two vertices are equal, if they have the same names.
        - If name is not supplied by the user, a name is automatically generated using "uuid" library.
        """

        def __init__(self, name=None):
            self._name = name if name is not None else str(uuid.uuid4())

        def __hash__(self):
            return self.name.__hash__()

        def __eq__(self, other):
            assert type(other) == type(self), f"Type mismatch: type(self)={type(self)}, type(other)={type(other)}."
            return self.name == other.name

        def __str__(self):
            return f"{self.__class__.__qualname__}(name={self.name})"

        def __repr__(self):
            obj_dict = dict()
            for key in self.__dict__.keys():
                value = self.__dict__[key]
                if not key.startswith('__') and not callable(value):
                    obj_dict[key] = value

            return obj_dict.__repr__()

        @property
        def name(self):
            return self._name

    class Edge(object):
        """
        Base class for representing a edge of graph.

        - :class:`Graph.Edge` represents a directed edge.
        - Two edges are equal, if the two :class:`Graph.Edge` objects are same.

        :param u: (:class:`Graph.Vertex` or its sub-class) Source vertex of edge.
        :param v: (:class:`Graph.Vertex` or its sub-class) Target vertex of edge.
        """

        def __init__(self, u: 'Graph.Vertex', v: 'Graph.Vertex'):
            self._source = u
            self._target = v
            self._name = (u, v)

        def __hash__(self):
            return self._name.__hash__()

        def __eq__(self, other):
            assert type(other) == type(self), f"Type mismatch: type(self)={type(self)}, type(other)={type(other)}."
            return self.name == other.name

        def __str__(self):
            return f"{self.__class__.__qualname__}(u={self.source}, v={self.target})"

        def __repr__(self):
            obj_dict = dict()
            for key in self.__dict__.keys():
                value = self.__dict__[key]
                if not key.startswith('__') and not callable(value):
                    obj_dict[key] = value

            return obj_dict.__repr__()

        @property
        def source(self):
            """ Returns the source vertex of edge. """
            return self._source

        @property
        def target(self):
            """ Returns the target vertex of edge. """
            return self._target

        @property
        def name(self):
            return self._name

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, vtype=None, etype=None, graph=None, file=None):

        # Validate vertex type. If okay, update the Vertex type of this instance
        if vtype is not None:
            assert issubclass(vtype, self.Vertex),  \
                f"Vertex type (Vertex) must be a sub-class of {self.__class__.__qualname__}." \
                f"Vertex class. Received {vtype.__qualname__}."

            self.Vertex = vtype

        # Validate edge type. If okay, update the Edge type of this instance
        if etype is not None:
            assert issubclass(etype, self.Edge),  \
                f"Edge type (etype) must be a sub-class of {self.__class__.__qualname__}.Edge " \
                f"class. Received {etype.__qualname__}."

            self.Edge = etype

        # # Validate input data-types
        # _class = self.__class__
        #
        # if Vertex is None:
        #     Vertex = _class.Vertex
        # else:
        #     assert issubclass(Vertex, self.Vertex), \
        #         f"Vertex must be a sub-class of {_class}.Vertex class. Received {Vertex}."
        #
        # if etype is None:
        #     etype = _class.Edge
        # else:
        #     assert issubclass(etype, self.Edge), \
        #         f"etype must be a sub-class of {_class}.Edge class. Received {etype}."

        # Define internal data structure
        self.vtype = self.Vertex                                    # Vertex class used in graph
        self.etype = self.Edge                                      # Edge class used in graph
        self._vertex_edge_map = dict()                              # Dict: {vertex: (set(<in-edge>), set(<out-edge>))}
        self._edges = set()                                         # Set of all edges of graph

        # TODO: Initialize graph by provided (optional) inputs
        if graph is not None and file is None:                      # pragma: no cover
            self._instantiate_by_graph(graph)

        # TODO: If file argument is given, then load graph from the file.
        elif file is not None and graph is None:                    # pragma: no cover
            self._load(filename=file)

        elif file is not None and graph is not None:
            raise ValueError("Input parameters 'file' and 'graph' should not be provided simultaneously.")

    def __eq__(self, other):
        assert type(self) == type(other), f"Type mismatch: type(self)={type(self)} and type(other)={type(other)}."
        return set(self.vertices) == set(other.vertices) and set(self.edges) == set(other.edges)

    def __repr__(self):
        return f"{self.__class__.__qualname__}(|V|={self.num_vertices} of type={self.Vertex.__qualname__}, " \
            f"|E|={self.num_edges} of type={self.Edge.__qualname__})"

    def __contains__(self, item):
        if isinstance(item, self.Vertex):
            return self.has_vertex(item)

        elif isinstance(item, self.Edge):
            return self.has_edge(item)

        else:
            raise TypeError(f"{self}.__contains__: Input must be of {type(self.Vertex)} or {type(self.Edge)}. "
                            f"Received {type(item)}.")

    __hash__ = object.__hash__

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def edges(self) -> Iterator:
        """ Returns an iterator over edges in graph. """
        return iter(self._edges)

    @property
    def is_multigraph(self):
        raise NotImplementedError(f"{self.__class__.__name__}.is_multigraph property is not yet implemented.")

    @property
    def num_edges(self) -> int:
        """ Returns the number of edges in graph. """
        return len(self._edges)

    @property
    def num_vertices(self) -> int:
        """ Returns the number of vertices in graph. """
        return len(self._vertex_edge_map)

    @property
    def vertices(self) -> Iterator:
        """ Returns an iterator over vertices in graph. """
        return iter(self._vertex_edge_map.keys())

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def add_vertex(self, v: 'Graph.Vertex'):
        """
        Adds a new vertex to graph.
        An attempt to add existing vertex will be ignored, with a warning.

        :param v: (:class:`Graph.Vertex`) Vertex to be added to graph.
        """
        assert isinstance(v, self.Vertex), \
            f"Vertex {v} must be object of {self.Vertex}. Given, v is {v.__class__.__name__}"

        # If vertex is not already added, then add it.
        if v not in self._vertex_edge_map:
            self._vertex_edge_map[v] = (set(), set())
        else:
            warnings.warn(f"Vertex {v} is already present in graph. Ignoring request to add.")

    def add_vertices(self, vbunch: Iterable['Graph.Vertex']):
        """
        Adds a bunch of vertices to graph.
        An attempt to add existing vertex will be ignored, with a warning.

        :param vbunch: (Iterable over :class:`Graph.Vertex`) Vertices to be added to graph.
        """
        for v in vbunch:
            self.add_vertex(v)

    def add_edge(self, e: 'Graph.Edge'):
        """
        Adds an edge to the graph.
        Both the vertices must be present in the graph.

        :param e: (:class:`Graph.Edge`) An edge to be added to the graph.
        :raises AttributeError: When at least one of the vertex is not in the graph.
        :raises AssertionError: When argument `e` is not an :class:`Graph.Edge` object.
        """
        assert isinstance(e, self.Edge), \
            f"Edge {e} must be an object of {self.Edge} class. Got {e.__class__.__name__}"

        if e in self._edges:
            warnings.warn(f"Edge {e} is already present in graph. Ignoring request to add.")
            return None

        u = e.source
        v = e.target

        if u in self._vertex_edge_map and v in self._vertex_edge_map:
            self._vertex_edge_map[u][1].add(e)
            self._vertex_edge_map[v][0].add(e)
            self._edges.add(e)
            return None

        if u not in self._vertex_edge_map and v not in self._vertex_edge_map:
            raise AssertionError(f"Vertices {u} and {v} are not in graph.")

        elif u in self._vertex_edge_map and v not in self._vertex_edge_map:
            raise AssertionError(f"Vertex {v} is not in graph.")

        else:   # v in self._vertex_edge_map:
            raise AssertionError(f"Vertex {u} is not in graph.")

    def add_edges(self, ebunch: Iterable['Graph.Edge']):
        """
        Adds a bunch of edges to the graph.
        Both the vertices of all edges must be present in the graph.

        :raises AttributeError: When at least one of the vertex is not in the graph.
        :raises AssertionError: When argument `e` is not an :class:`Graph.Edge` object.
        """
        for e in ebunch:
            self.add_edge(e)

    def get_edges(self, u: 'Graph.Vertex', v: 'Graph.Vertex'):
        """
        Returns all edges with source ``u`` and target ``v``.

        :param u: (:class:`Graph.Vertex`) Vertex of the graph.
        :param v: (:class:`Graph.Vertex`) Vertex of the graph.
        :return: (iterator(:class:`Graph.Edge`)) Edges between u, v.
        """
        assert u in self, f"{self}.get_edges:: Vertex u={u} is not in graph."
        assert v in self, f"{self}.get_edges:: Vertex v={v} is not in graph."
        return iter(set.intersection(self._vertex_edge_map[u][1], self._vertex_edge_map[v][0]))

    def has_edge(self, e: 'Graph.Edge'):
        """
        Checks whether the graph has the given edge or not.

        :param e: (:class:`Graph.Edge`) An edge to be checked for containment in the graph.
        :return: (bool) True if the graph has the given edge, False otherwise.
        """
        return e in self._edges

    def has_vertex(self, v: 'Graph.Vertex'):
        """
        Checks whether the graph has the given vertex or not.

        :param v: (:class:`Graph.Vertex`) Vertex to be checked for containment.
        :return: (bool) True if given vertex is in the graph, else False.
        """
        return v in self._vertex_edge_map.keys()

    def in_edges(self, v: Union['Graph.Vertex', Iterable['Graph.Vertex']]):
        """
        Returns an iterator over incoming edges to given vertex or vertices.
        In case of vertices, the iterator is defined over the union of set of
        incoming edges of individual vertices.

        :param v: (:class:`Graph.Vertex`) Vertex of graph.

        :raises AssertionError: When `v` is neither a :class:`Graph.Vertex` object
            nor an iterable of :class:`Graph.Vertex` objects.
        """
        if isinstance(v, self.Vertex):
            assert isinstance(v, self.Vertex), f"All vertices in input: {v} must be of type={self.Vertex}."
            return iter(self._vertex_edge_map[v][0])

        elif isinstance(v, Iterable):
            assert all(isinstance(u, self.Vertex) for u in v), \
                f"All vertices in input: {v} must be of type={self.Vertex}."

            in_edges = (self._vertex_edge_map[u][0] for u in v)
            return iter(reduce(set.union, in_edges))

        raise AssertionError(f"Vertex {v} must be a single or an iterable of {self.Vertex} objects.")

    def in_neighbors(self, v: Union['Graph.Vertex', Iterable['Graph.Vertex']]):
        """
        Returns an iterator over sources of incoming edges to given vertex or vertices.
        In case of vertices, the iterator is defined over the union of set of
        incoming edges of individual vertices.

        :param v: (:class:`Graph.Vertex`) Vertex of graph.

        :raises AssertionError: When `v` is neither a :class:`Graph.Vertex` object
            nor an iterable of :class:`Graph.Vertex` objects.
        """
        if isinstance(v, self.Vertex):
            assert isinstance(v, self.Vertex), f"All vertices in input: {v} must be of type={self.Vertex}."
            return iter(e.source for e in self._vertex_edge_map[v][0])

        elif isinstance(v, Iterable):
            assert all(isinstance(u, self.Vertex) for u in v), \
                f"All vertices in input: {v} must be of type={self.Vertex}."

            return iter(e.source for u in v for e in self._vertex_edge_map[u][0])

        raise AssertionError(f"Vertex {v} must be a single or an iterable of {self.Vertex} objects.")

    def prune(self, v: 'Graph.Vertex'):
        raise NotImplementedError

    def out_edges(self, v: Union['Graph.Vertex', Iterable['Graph.Vertex']]):
        """
        Returns an iterator over outgoing edges to given vertex or vertices.
        In case of vertices, the iterator is defined over the union of set of
        incoming edges of individual vertices.

        :param v: (:class:`Graph.Vertex`) Vertex of graph.

        :raises AssertionError: When `v` is neither a :class:`Graph.Vertex` object
            nor an iterable of :class:`Graph.Vertex` objects.
        """
        if isinstance(v, self.Vertex):
            assert isinstance(v, self.Vertex), f"All vertices in input: {v} must be of type={self.Vertex}."
            return iter(self._vertex_edge_map[v][1])

        elif isinstance(v, Iterable):
            assert all(isinstance(u, self.Vertex) for u in v), \
                f"All vertices in input: {v} must be of type={self.Vertex}."

            out_edges = (self._vertex_edge_map[u][1] for u in v)
            return iter(reduce(set.union, out_edges))

        raise AssertionError(f"Vertex {v} must be a single or an iterable of {self.Vertex} objects.")

    def out_neighbors(self, v: Union['Graph.Vertex', Iterable['Graph.Vertex']]):
        """
        Returns an iterator over targets of incoming edges to given vertex or vertices.
        In case of vertices, the iterator is defined over the union of set of
        incoming edges of individual vertices.

        :param v: (:class:`Graph.Vertex`) Vertex of graph.

        :raises AssertionError: When `v` is neither a :class:`Graph.Vertex` object
            nor an iterable of :class:`Graph.Vertex` objects.
        """
        if isinstance(v, self.Vertex):
            assert isinstance(v, self.Vertex), f"All vertices in input: {v} must be of type={self.Vertex}."
            return iter(e.target for e in self._vertex_edge_map[v][1])

        elif isinstance(v, Iterable):
            assert all(isinstance(u, self.Vertex) for u in v), \
                f"All vertices in input: {v} must be of type={self.Vertex}."

            return iter(e.target for u in v for e in self._vertex_edge_map[u][1])

        raise AssertionError(f"Vertex {v} must be a single or an iterable of {self.Vertex} objects.")

    def rm_vertex(self, v: 'Graph.Vertex'):
        """
        Removes a vertex from the graph.
        An attempt to remove a non-existing vertex will be ignored, with a warning.

        :param v: (:class:`Graph.Vertex`) Vertex to be removed.
        """
        assert isinstance(v, self.Vertex), \
            f"Vertex {v} must be object of {self.Vertex}. Given, v is {v.__class__.__name__}"

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

        :param vbunch: (Iterable over :class:`Graph.Vertex`) Vertices to be removed.
        """
        for v in vbunch:
            self.rm_vertex(v)

    def rm_edge(self, e: 'Graph.Edge'):
        """
        Removes an edge from the graph.
        An attempt to remove a non-existing edge will be ignored, with a warning.

        :param e: (:class:`Graph.Edge`) Edge to be removed.
        """
        # Check the type of input edge
        assert isinstance(e, Graph.Edge), \
            f"e must be an object of {self.__class__.__name__}.Edge class or its sub-class. Got {e.__class__.__name__}"

        # If edge is not in graph, warn the user and return
        if e not in self._edges:
            warnings.warn(f"Edge {e} is not present in graph. Ignoring request to remove edge.")
            return None

        # Extract source and target of edge
        u = e.source
        v = e.target

        # Remove the edge
        self._vertex_edge_map[u][1].remove(e)
        self._vertex_edge_map[v][0].remove(e)
        self._edges.remove(e)

    def rm_edges(self, ebunch: Iterable['Graph.Edge']):
        """
        Removes a bunch of edges from the graph.
        An attempt to remove a non-existing edge will be ignored, with a warning.

        :param ebunch: (Iterable over :class:`Graph.Edge`) Edges to be removed.
        """
        for e in ebunch:
            self.rm_edge(e)

    def save(self, fname: str = None, ext: str = 'graphml'):
        assert "." not in fname, "fname (file name) cannot contain a dot '.'"
        parser = GraphMLParser(graph=self)
        parser.write(".".join([fname, ext]))

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


