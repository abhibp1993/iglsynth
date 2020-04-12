"""
iglsynth: graph.py

License goes here...
"""

from typing import Iterable, Iterator, Union
from functools import reduce
import logging
import iglsynth.util.entity as entity


__all__ = ["Vertex", "Edge", "Graph", "SubGraph"]


class IGLDict(dict):
    def __init__(self, name, *args, **kwargs):
        super(IGLDict, self).__init__(*args, **kwargs)
        self._name = name

        # Get a logger for IGLDict
        logger = logging.getLogger(self.__module__)
        self.logger = logger

    def __setitem__(self, key, value):
        super(IGLDict, self).__setitem__(key, value)
        self.logger.info(f"Updating IGLDict:\n\tself:{self}\n\tkey={key}\n\tvalue={value}")

    def __delitem__(self, key):
        # Check if key is in dictionary
        is_in_dict = self.__contains__(key)

        # Remove key
        super(IGLDict, self).__delitem__(key)

        # Log if key was removed
        if is_in_dict and not self.__contains__(key):
            self.logger.info(f"Removing {key} from IGLDict({self._name}).")


class IGLSet(set):
    def __init__(self, name, *args, **kwargs):
        super(IGLSet, self).__init__(*args, **kwargs)
        self._name = name

        # Get a logger for IGLDict
        logger = logging.getLogger(self.__module__)
        self.logger = logger

    def add(self, element):
        super(IGLSet, self).add(element)
        self.logger.info(f"Updating IGLSet:\n\tself:{self}\n\tnewitem={element}")

    def remove(self, key):
        # Check if key is in dictionary
        is_in_dict = self.__contains__(key)

        # Remove key
        super(IGLSet, self).remove(key)

        # Log if key was removed
        if is_in_dict and not self.__contains__(key):
            self.logger.info(f"Removing {key} from IGLSet({self._name}).")


class Vertex(entity.Entity):
    def __init__(self, name=None, **kwargs):
        super(Vertex, self).__init__(name=name, **kwargs)


class Edge(entity.Entity):
    def __init__(self, u, v, **kwargs):
        # Default naming for an edge (note: it's a tuple, not a string)
        if "name" not in kwargs:
            name = (u, v)
        else:
            name = kwargs["name"]

        # Base class constructor
        super(Edge, self).__init__(name=name, **kwargs)

        # Edge data structure
        self._u = u
        self._v = v

        # Log the creation of edge
        self.logger.info(f"Created {self}.")

    @property
    def source(self):
        return self._u

    @property
    def target(self):
        return self._v


class GraphBase(entity.Entity):
    def __setattr__(self, key, value):
        if key == "Vertex":
            assert issubclass(value, Vertex), \
                f"Cannot set {self.__class__.__qualname__}.Vertex = {value}. " \
                f"{value} should be a subclass of {Vertex} class."

        if key == "Edge":
            assert issubclass(value, Edge), \
                f"Cannot set {self.__class__.__qualname__}.Edge = {value}. " \
                f"{value} should be a subclass of {Vertex} class."

        super(GraphBase, self).__setattr__(key, value)


class Graph(GraphBase):
    Vertex = Vertex
    Edge = Edge

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, name=None, **kwargs):
        # Entity constructor
        super(Graph, self).__init__(name=name, **kwargs)

        # Graph data structure
        self._edges = set()
        self._ve_map_in = IGLDict(name=f"{self}._ve_map_in")
        self._ve_map_out = IGLDict(name=f"{self}._ve_map_out")

        # Log event of creation
        self.logger.info(f"Graph object {self} is created.")

    def __contains__(self, item):
        if issubclass(type(item), Vertex):
            return self.has_vertex(item)

        if issubclass(type(item), Edge):
            return self.has_edge(item)

        raise TypeError(f"Graph containment checking expected {self.Vertex} or {self.Edge} objects. "
                        f"Received {type(item)}.")

    def __repr__(self):
        return f"{self._class_name}(name={self.name}, |V|={self.num_vertices}, |E|={self.num_edges})"

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def edges(self):
        """ Returns an iterator over edges in graph. """
        return iter(self._edges)

    # @property
    # def is_multigraph(self):
    #     raise NotImplementedError(f"{self.__class__.__name__}.is_multigraph property is not yet implemented.")

    @property
    def num_edges(self):
        """ Returns the number of edges in graph. """
        return len(self._edges)

    @property
    def num_vertices(self):
        """ Returns the number of vertices in graph. """
        return len(self._ve_map_in)

    @property
    def vertices(self) -> Iterator:
        """ Returns an iterator over vertices in graph. """
        return iter(self._ve_map_in.keys())

    # @property
    # def gprop_names(self):
    #     raise NotImplementedError()
    #
    # @property
    # def gprop_dict(self):
    #     raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def add_vertex(self, v):
        """
        Adds a new vertex to graph.
        An attempt to add existing vertex will be ignored, with a warning.
        :param v: (:class:`Graph.Vertex`) Vertex to be added to graph.
        """
        # Type checking
        assert isinstance(v, self.Vertex), f"Given vertex {v} must be an instance of {self}.Vertex class. "

        # If vertex is not already added, then add it.
        if not self.has_vertex(v):
            self._ve_map_in[v] = IGLSet(name=f"{self}._ve_map_in[{v}]")
            self._ve_map_out[v] = IGLSet(name=f"{self}._ve_map_out[{v}]")
            self.logger.info(f"Vertex {v} is added to {self}.")
        else:
            self.logger.debug(f"Vertex {v} is already present in {self}. Ignoring request to add.")

    def add_vertices(self, vbunch):
        """
        Adds a bunch of vertices to graph.
        An attempt to add existing vertex will be ignored, with a warning.
        :param vbunch: (Iterable over :class:`Graph.Vertex`) Vertices to be added to graph.
        """
        for v in vbunch:
            self.add_vertex(v)

    def add_edge(self, e):
        """
        Adds an edge to the graph.
        Both the vertices must be present in the graph.
        :param e: (:class:`Graph.Edge`) An edge to be added to the graph.
        :raises AttributeError: When at least one of the vertex is not in the graph.
        :raises AssertionError: When argument `e` is not an :class:`Graph.Edge` object.
        """
        # Type checking
        assert isinstance(e, self.Edge), f"Given edge {e} must be an instance of {self}.Edge class. "

        # Ignore duplicate addition of edge
        if self.has_edge(e):
            self.logger.debug(f"Edge {e} is already present in {self}. Ignoring request to add.")
            return None

        # Get source and target vertices
        u = e.source
        v = e.target

        # Update graph data structure
        if self.has_vertex(u) and self.has_vertex(v):
            self._ve_map_out[u].add(e)
            self._ve_map_in[v].add(e)
            self._edges.add(e)
            self.logger.info(f"Edge {e} is added to {self}.")
            return None

        if not self.has_vertex(u) and not self.has_vertex(v):
            raise AssertionError(f"Vertices {u} and {v} are not in graph.")

        elif self.has_vertex(u) and not self.has_vertex(u):
            raise AssertionError(f"Vertex {v} is not in graph.")

        else:  # not self.has_vertex(u):
            raise AssertionError(f"Vertex {u} is not in graph.")

    def add_edges(self, ebunch):
        """
        Adds a bunch of edges to the graph.
        Both the vertices of all edges must be present in the graph.
        :raises AttributeError: When at least one of the vertex is not in the graph.
        :raises AssertionError: When argument `e` is not an :class:`Graph.Edge` object.
        """
        for e in ebunch:
            self.add_edge(e)

    def get_edges(self, u, v=None):
        """
        Returns all edges with source ``u`` and target ``v``.
        :param u: (:class:`Graph.Vertex`) Vertex of the graph.
        :param v: (:class:`Graph.Vertex`) Vertex of the graph.
        :return: (iterator(:class:`Graph.Edge`)) Edges between u, v.
        """
        assert self.has_vertex(u), f"Vertex u={u} is not in graph."
        assert self.has_vertex(v), f"Vertex v={v} is not in graph."

        if v is None:
            return iter(self._ve_map_out[u])

        return iter(set.intersection(self._ve_map_out[u], self._ve_map_in[v]))

    def has_edge(self, e):
        """
        Checks whether the graph has the given edge or not.
        :param e: (:class:`Graph.Edge`) An edge to be checked for containment in the graph.
        :return: (bool) True if the graph has the given edge, False otherwise.
        """
        return e in self._edges

    def has_vertex(self, v):
        """
        Checks whether the graph has the given vertex or not.
        :param v: (:class:`Graph.Vertex`) Vertex to be checked for containment.
        :return: (bool) True if given vertex is in the graph, else False.
        """
        # Check for data corruption
        if (v in self._ve_map_in and v not in self._ve_map_out) or (v not in self._ve_map_in and v in self._ve_map_out):
            raise RuntimeError(f"Graph data structure is corrupted. "
                               f"({v} in self._ve_map_in and {v} not in self._ve_map_out)="
                               f"{(v in self._ve_map_in and v not in self._ve_map_out)}. "
                               f"({v} not in self._ve_map_in and {v} in self._ve_map_out)="
                               f"{(v not in self._ve_map_in and v in self._ve_map_out)}. "
                               )

        return v in self._ve_map_in

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
            assert self.has_vertex(v), f"Vertex {v} is not in {self}."
            return iter(self._ve_map_in[v])

        elif isinstance(v, Iterable):
            assert all(self.has_vertex(u) for u in v), \
                f"All vertices in input: {v} must be in {self}."

            in_edges = (self._ve_map_in[u] for u in v)
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
        return iter(e.source for e in self.in_edges(v))

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
            assert self.has_vertex(v), f"Vertex {v} is not in {self}."
            return iter(self._ve_map_out[v])

        elif isinstance(v, Iterable):
            assert all(self.has_vertex(u) for u in v), \
                f"All vertices in input: {v} must be in {self}."

            out_edges = (self._ve_map_out[u] for u in v)
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
        return iter(e.target for e in self.out_edges(v))

    def rm_edge(self, e: 'Graph.Edge'):
        """
        Removes an edge from the graph.
        An attempt to remove a non-existing edge will be ignored, with a warning.
        :param e: (:class:`Graph.Edge`) Edge to be removed.
        """
        # Check the type of input edge
        assert isinstance(e, self.Edge), \
            f"e must be an object of {self._class_name}.Edge class or its sub-class. Got {e.__class__.__name__}"

        # If edge is not in graph, warn the user and return
        if e not in self:
            self.logger.debug(f"Edge {e} is not present in {self}. Ignoring request to remove edge.")
            return None

        # Extract source and target of edge
        u = e.source
        v = e.target

        # Remove the edge
        self._ve_map_out[u].remove(e)
        self._ve_map_in[v].remove(e)
        self._edges.remove(e)

        # Log the removal of edge
        self.logger.info(f"Edge {e} was removed from {self}")

    def rm_edges(self, ebunch: Iterable['Graph.Edge']):
        """
        Removes a bunch of edges from the graph.
        An attempt to remove a non-existing edge will be ignored, with a warning.
        :param ebunch: (Iterable over :class:`Graph.Edge`) Edges to be removed.
        """
        for e in ebunch:
            self.rm_edge(e)

    def rm_vertex(self, v: 'Graph.Vertex'):
        """
        Removes a vertex from the graph.
        An attempt to remove a non-existing vertex will be ignored, with a warning.
        :param v: (:class:`Graph.Vertex`) Vertex to be removed.
        """
        assert isinstance(v, self.Vertex), \
            f"Vertex {v} must be object of {self.Vertex}. Given, v is {v.__class__.__name__}"

        # Remove incoming and outgoing edges from v, and then remove v
        if self.has_vertex(v):
            in_edges = self.in_edges(v)
            out_edges = self.out_edges(v)

            self.rm_edges(in_edges)
            self.rm_edges(out_edges)
            self._ve_map_in.pop(v)
            self._ve_map_out.pop(v)

            self.logger.debug(f"Vertex {v} was removed from {self}.")
        else:
            self.logger.debug(f"Vertex {v} is not present in {self}. Ignoring request to remove vertex.")

    def rm_vertices(self, vbunch: Iterable['Graph.Vertex']):
        """
        Removes a bunch of vertices from the graph.
        An attempt to remove a non-existing vertex will be ignored, with a warning.
        :param vbunch: (Iterable over :class:`Graph.Vertex`) Vertices to be removed.
        """
        for v in vbunch:
            self.rm_vertex(v)

    def serialize(self, ignores=tuple()):
        return super(Graph, self).serialize(ignores=list(ignores) + [])


class SubGraph(Graph):

    def __init__(self, graph, name=None):

        # Type checking
        assert isinstance(graph, Graph), f"Input graph must be an instance of Graph or its subclass."

        # Set name of sub-graph
        if name is None and graph.name is not None:
            name = f"SubGraph({graph})"
        
        super(SubGraph, self).__init__(name)

        # Rebind sub-graph internal variables to point to graph's internal variables
        self._graph = graph
        self._edges = graph._edges
        self._ve_map_in = graph._ve_map_in
        self._ve_map_out = graph._ve_map_out
        self._vfilt = set()
        self._efilt = set()
        self._is_vfilt_set = False
        self._is_efilt_set = False

    def __contains__(self, item):
        if issubclass(type(item), Vertex):
            try:
                return self.has_vertex(item)
            except NotImplementedError:
                self.logger.debug(f"SubGraph.has_vertex({item}) accesses without user definition.")
                if self._is_vfilt_set:
                    return item in self._vfilt
                return super(SubGraph, self).__contains__(item)

        if issubclass(type(item), Edge):
            try:
                return self.has_edge(item)
            except NotImplementedError:
                self.logger.debug(f"SubGraph.has_edge({item}) accesses without user definition.")
                if self._is_efilt_set:
                    return item in self._efilt
                return super(SubGraph, self).__contains__(item)

        raise TypeError(f"Graph containment checking expected {self.Vertex} or {self.Edge} objects. "
                        f"Received {type(item)}.")

    def add_vertex(self, v):
        """
        Adds a new vertex to graph.
        An attempt to add existing vertex will be ignored, with a warning.
        :param v: (:class:`Graph.Vertex`) Vertex to be added to graph.
        """
        raise TypeError(f"New vertex cannot be added to a sub-graph.")

    def add_edge(self, e):
        """
        Adds an edge to the graph.
        Both the vertices must be present in the graph.
        :param e: (:class:`Graph.Edge`) An edge to be added to the graph.
        :raises AttributeError: When at least one of the vertex is not in the graph.
        :raises AssertionError: When argument `e` is not an :class:`Graph.Edge` object.
        """
        raise TypeError(f"New edge cannot be added to a sub-graph.")

    def freeze(self):
        # Generate vfilt and efilt Boolean maps
        vfilt = {True if v in self else False for v in self._graph.vertices}
        efilt = {True if e in self else False for e in self._graph.edges}

        # Set vfilt and efilt
        self.set_vfilt(vfilt)
        self.set_efilt(efilt)

    def get_edges(self, u, v=None):
        """
        Returns all edges with source ``u`` and target ``v``.
        :param u: (:class:`Graph.Vertex`) Vertex of the graph.
        :param v: (:class:`Graph.Vertex`) Vertex of the graph.
        :return: (iterator(:class:`Graph.Edge`)) Edges between u, v.
        """
        assert u in self, f"Vertex u={u} is not in graph."
        assert v in self, f"Vertex v={v} is not in graph."

        if v is None:
            return iter(self._ve_map_out[u])

        return iter(set.intersection(self._ve_map_out[u], self._ve_map_in[v]))

    def has_edge(self, e):
        """
        Checks whether the graph has the given edge or not.
        :param e: (:class:`Graph.Edge`) An edge to be checked for containment in the graph.
        :return: (bool) True if the graph has the given edge, False otherwise.
        """
        raise NotImplementedError("User must redefine 'has_edge' function to implement edge filtering")

    def has_vertex(self, v):
        """
        Checks whether the graph has the given vertex or not.
        :param v: (:class:`Graph.Vertex`) Vertex to be checked for containment.
        :return: (bool) True if given vertex is in the graph, else False.
        """
        raise NotImplementedError("User must redefine 'has_edge' function to implement edge filtering")

    def rm_edge(self, e: 'Graph.Edge'):
        """
        Removes an edge from the graph.
        An attempt to remove a non-existing edge will be ignored, with a warning.
        :param e: (:class:`Graph.Edge`) Edge to be removed.
        """
        raise TypeError(f"Vertex cannot be removed from a sub-graph. "
                        f"Operation should be performed on underlying graph.")

    def rm_vertex(self, v: 'Graph.Vertex'):
        """
        Removes a vertex from the graph.
        An attempt to remove a non-existing vertex will be ignored, with a warning.
        :param v: (:class:`Graph.Vertex`) Vertex to be removed.
        """
        raise TypeError(f"Vertex cannot be removed from a sub-graph. "
                        f"Operation should be performed on underlying graph.")

    def serialize(self, ignores=None):
        # Freeze the sub-graph
        self.freeze()

        # Generate dictionary for serialization
        return super(Graph, self).serialize(ignores=list(ignores) + [])

    def set_vfilt(self, vfilt):
        self._vfilt = set(vfilt)
        self._is_vfilt_set = True

    def set_efilt(self, efilt):
        self._efilt = set(efilt)
        self._is_efilt_set = True
