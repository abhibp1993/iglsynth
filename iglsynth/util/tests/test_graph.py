import pytest
from iglsynth.util.graph import *


def test_graph_instantiation():
    # 1. Default Constructor
    _ = Graph()

    # 2. Constructor with UserVertex, UserEdge types
    class UserVertex(Graph.Vertex):
        def __init__(self, name):
            self.id = name

    class UserEdge(Graph.Edge):
        def __init__(self, name, u, v):
            super(UserEdge, self).__init__(u, v)
            self.id = name

    _ = Graph(vtype=UserVertex, etype=UserEdge)

    with pytest.raises(AssertionError):
        _ = Graph(vtype=UserEdge, etype=UserVertex)

    # 3. Copy Constructor -- TODO
    # graph = Graph(graph=graph)

    # 4. Load Graph -- TODO
    # graph = Graph(file="")
    # graph = Graph(vtype=UserVertex, etype=UserEdge, file="")


def test_add_vertex():
    graph = Graph()

    # Using default vertex type
    graph.add_vertex(Graph.Vertex())
    assert graph.num_vertices == 1

    # Using user-defined vertex class
    class UserVertex(Graph.Vertex):
        pass

    graph.add_vertex(UserVertex())
    assert graph.num_vertices == 2

    # Using an arbitrary class other than Graph.Vertex or its derivative.
    with pytest.raises(AssertionError):
        graph.add_vertex(10)


def test_add_vertices():
    graph = Graph()

    v0 = Graph.Vertex()
    v1 = Graph.Vertex()

    graph.add_vertices([v0, v1])

    with pytest.raises(AssertionError):
        graph.add_vertex([v0, 10])


def test_rm_vertex():
    graph = Graph()

    v0 = Graph.Vertex()
    v1 = Graph.Vertex()

    graph.add_vertices([v0, v1])

    # Remove one vertex
    graph.rm_vertex(v0)
    assert graph.num_vertices == 1
    assert v0 not in list(graph.vertices)

    # Remove an absent vertex
    graph.rm_vertex(v0)
    assert graph.num_vertices == 1
    assert v0 not in list(graph.vertices)

    # Remove another vertex
    graph.rm_vertex(v1)
    assert graph.num_vertices == 0
    assert v0 not in list(graph.vertices)
    assert v1 not in list(graph.vertices)

    # Remove from empty graph
    graph.rm_vertex(v1)
    assert graph.num_vertices == 0
    assert v0 not in list(graph.vertices)
    assert v1 not in list(graph.vertices)

    with pytest.raises(AssertionError):
        graph.rm_vertex(10)


def test_rm_vertices():
    graph = Graph()

    v0 = Graph.Vertex()
    v1 = Graph.Vertex()

    graph.add_vertices([v0, v1])

    # Remove one vertex
    graph.rm_vertices([v0, v1])
    assert graph.num_vertices == 0
    assert v0 not in list(graph.vertices)
    assert v1 not in list(graph.vertices)

    with pytest.raises(AssertionError):
        graph.rm_vertex([10, v0])


def test_has_vertex():

    # Default graph class
    graph = Graph()
    v0 = Graph.Vertex()
    v1 = Graph.Vertex()
    v2 = Graph.Vertex()
    graph.add_vertices([v0, v1])

    assert graph.has_vertex(v0)
    assert graph.has_vertex(v1)
    assert not graph.has_vertex(v2)

    assert v0 in graph
    assert v1 in graph
    assert v2 not in graph

    # Graph class with custom vertex class
    class UserVertex(Graph.Vertex):
        def __init__(self, id):
            super(UserVertex, self).__init__()
            self.id = id

    graph = Graph(vtype=UserVertex)
    v0 = UserVertex(id="v0")
    v1 = UserVertex(id="v1")

    graph.add_vertex(v0)

    assert graph.has_vertex(v0)
    assert not graph.has_vertex(v1)

    assert v0 in graph
    assert v1 not in graph

    # Derived Graph class with custom vertex class
    class NewGraph(Graph):
        class Vertex(Graph.Vertex):
            def __init__(self, name):
                super(NewGraph.Vertex, self).__init__(name)

    graph = NewGraph()
    v0 = graph.Vertex(name="v0")
    v1 = graph.Vertex(name="v1")
    v2 = graph.Vertex(name="v2")
    graph.add_vertices([v0, v1])

    assert graph.has_vertex(v0)
    assert graph.has_vertex(v1)
    assert not graph.has_vertex(v2)

    assert v0 in graph
    assert v1 in graph
    assert v2 not in graph


def test_add_edge():
    graph = Graph()
    v0 = Graph.Vertex()
    v1 = Graph.Vertex()
    graph.add_vertices([v0, v1])

    # Add an edge
    e = Graph.Edge(v0, v1)
    graph.add_edge(e)
    assert graph.num_edges == 1

    # Attempt repeat addition of same edge
    graph.add_edge(e)
    assert graph.num_edges == 1

    # Note: The following case is now resolved. Two edges are equal, if their names are equal.
    # # Add a new edge between same vertices
    # e0 = Graph.Edge(v0, v1)
    # graph.add_edge(e0)
    # assert graph.num_edges == 2

    # Add edge using UserDefined Edge type
    class UserEdge(Graph.Edge):
        def __init__(self, name, u, v):
            super(UserEdge, self).__init__(u, v)
            self.id = name

    graph = Graph(etype=UserEdge)
    v0 = Graph.Vertex()
    v1 = Graph.Vertex()
    graph.add_vertices([v0, v1])

    graph.add_edge(UserEdge(name="edge", u=v0, v=v1))
    assert graph.num_edges == 1

    with pytest.raises(AssertionError):
        graph.add_edge((0, 1))

    with pytest.raises(AssertionError):
        graph.add_edge(UserEdge(name="edge", u=v0, v=10))

    with pytest.raises(AssertionError):
        graph.add_edge(UserEdge(name="edge", u=10, v=v0))

    with pytest.raises(AssertionError):
        graph.add_edge(UserEdge(name="edge", u=90, v=10))


def test_add_edges():
    graph = Graph()
    v0 = Graph.Vertex()
    v1 = Graph.Vertex()
    graph.add_vertices([v0, v1])

    # Add multiple edges
    e0 = Graph.Edge(v0, v1)
    e1 = Graph.Edge(v0, v0)

    graph.add_edges([])
    assert graph.num_edges == 0

    graph.add_edges([e0])
    assert graph.num_edges == 1

    graph.add_edges([e0, e1])
    assert graph.num_edges == 2

    with pytest.raises(AssertionError):
        graph.add_edges((0, 1))

    with pytest.raises(AssertionError):
        graph.add_edge(graph.Edge(u=v0, v=10))

    with pytest.raises(AssertionError):
        graph.add_edge(graph.Edge(u=10, v=v0))

    with pytest.raises(AssertionError):
        graph.add_edge(graph.Edge(u=90, v=10))


def test_rm_edge():
    """
    .. note: rm_edge should never raise a KeyError (while removing some edge
        from vertex-edge-map. If this happens, check add_edge function to ensure
        whether the vertex-edge-map is properly handled or not.
    """
    graph = Graph()

    v0 = Graph.Vertex()
    v1 = Graph.Vertex()
    graph.add_vertices([v0, v1])

    e00 = Graph.Edge(v0, v0)
    e01 = Graph.Edge(v0, v1)
    e11 = Graph.Edge(v1, v1)
    graph.add_edges([e00, e01, e11])

    assert graph.num_edges == 3

    graph.rm_edge(e00)
    assert graph.num_edges == 2
    assert e00 not in list(graph.edges) and e01 in list(graph.edges) and e11 in list(graph.edges)

    graph.rm_edge(e00)
    assert graph.num_edges == 2
    assert e00 not in list(graph.edges) and e01 in list(graph.edges) and e11 in list(graph.edges)

    graph.rm_edges([e01, e11])
    assert graph.num_edges == 0
    assert e00 not in list(graph.edges) and e01 not in list(graph.edges) and e11 not in list(graph.edges)

    with pytest.raises(AssertionError):
        graph.rm_edge(10)

    with pytest.warns(UserWarning):
        graph.rm_edge(e01)


def test_rm_edges():
    """
    .. note: rm_edge should never raise a KeyError (while removing some edge
        from vertex-edge-map. If this happens, check add_edge function to ensure
        whether the vertex-edge-map is properly handled or not.
    """
    graph = Graph()

    v0 = Graph.Vertex()
    v1 = Graph.Vertex()
    graph.add_vertices([v0, v1])

    e00 = Graph.Edge(v0, v0)
    e01 = Graph.Edge(v0, v1)
    e11 = Graph.Edge(v1, v1)
    graph.add_edges([e00, e01, e11])

    # Remove edges
    graph.rm_edges([e01, e11])
    assert graph.num_edges == 1
    assert e00 in list(graph.edges) and e01 not in list(graph.edges) and e11 not in list(graph.edges)


def test_has_edge():

    # Default graph class
    graph = Graph()

    v0 = Graph.Vertex()
    v1 = Graph.Vertex()
    v2 = Graph.Vertex()

    e01 = Graph.Edge(v0, v1)
    e02 = Graph.Edge(v0, v2)

    graph.add_vertices([v0, v1])
    graph.add_edge(e01)

    assert graph.has_edge(e01)
    assert not graph.has_edge(e02)

    assert e01 in graph
    assert e02 not in graph

    # Graph class with custom vertex class
    class UserEdge(Graph.Edge):
        def __init__(self, name, u, v):
            self.id = name
            super(UserEdge, self).__init__(u, v)

    graph = Graph(etype=UserEdge)

    v0 = graph.Vertex()
    v1 = graph.Vertex()
    v2 = graph.Vertex()

    e01 = graph.etype(name="e01", u=v0, v=v1)
    e02 = graph.etype(name="e01", u=v0, v=v2)

    graph.add_vertices([v0, v1])
    graph.add_edge(e01)

    assert graph.has_edge(e01)
    assert not graph.has_edge(e02)

    assert e01 in graph
    assert e02 not in graph

    # Derived Graph class with custom vertex class
    class NewGraph(Graph):
        class Edge(Graph.Edge):
            def __init__(self, name, u, v):
                super(NewGraph.Edge, self).__init__(u, v)

    graph = NewGraph()

    v0 = graph.Vertex()
    v1 = graph.Vertex()
    v2 = graph.Vertex()

    e01 = graph.Edge("e01", v0, v1)
    e02 = graph.Edge("e01", v0, v2)

    graph.add_vertices([v0, v1])
    graph.add_edge(e01)

    assert graph.has_edge(e01)
    assert not graph.has_edge(e02)

    assert e01 in graph
    assert e02 not in graph

    with pytest.raises(TypeError):
        assert 10 in graph


def test_get_edges():

    graph = Graph()

    v0 = Graph.Vertex()
    v1 = Graph.Vertex()
    v2 = Graph.Vertex()
    graph.add_vertices([v0, v1])

    e00 = Graph.Edge(v0, v0)
    e01 = Graph.Edge(v0, v1)
    e11 = Graph.Edge(v1, v1)
    e11_2 = Graph.Edge(v1, v1)
    graph.add_edges([e00, e01, e11, e11_2])

    # Empty edge retrieval
    assert len(list(graph.get_edges(v1, v0))) == 0

    # Single edge retrieval
    assert len(list(graph.get_edges(v0, v1))) == 1

    # Multi edge retrieval
    assert len(list(graph.get_edges(v1, v1))) == 1

    # One or more vertices not in graph
    with pytest.raises(AssertionError):
        assert len(list(graph.get_edges(v1, v2))) == 0


def test_graph_properties():
    # Create a graph instance
    class UserVertex(Graph.Vertex):
        def __init__(self, name):
            super(UserVertex, self).__init__(name)

        def __repr__(self):
            return self.name

    class UserEdge(Graph.Edge):
        def __init__(self, u, v):
            self.id = f"({u}, {v})"
            super(UserEdge, self).__init__(u, v)

        def __repr__(self):
            return self.name

    graph = Graph(vtype=UserVertex, etype=UserEdge)

    # Add vertices and edges
    v1, v2, v3 = list(map(UserVertex, ['a', 'b', 'c']))
    graph.add_vertices([v1, v2, v3])

    e1, e2, e3, e4 = list(map(UserEdge, [v1, v2, v3, v1], [v2, v3, v1, v1]))
    graph.add_edges([e1, e2, e3, e4])

    # Test properties
    assert graph.num_vertices == 3
    assert graph.num_edges == 4
    assert set(graph.vertices) == {v1, v2, v3}
    assert set(graph.edges) == {e1, e2, e3, e4}

    # TODO assert graph.is_multigraph


def test_graph_neighbors():

    # Define a graph
    graph = Graph()

    v0 = Graph.Vertex()
    v1 = Graph.Vertex()
    graph.add_vertices([v0, v1])

    e00 = Graph.Edge(v0, v0)
    e01 = Graph.Edge(v0, v1)
    e11 = Graph.Edge(v1, v1)
    graph.add_edges([e00, e01, e11])

    # Check in-neighbors
    assert v0 in graph.in_neighbors(v=v0)
    assert v1 not in graph.in_neighbors(v=v0)
    assert v1 in graph.in_neighbors(v=v1)
    assert v0 in graph.in_neighbors(v=v1)

    assert v0 in graph.in_neighbors([v0, v1])
    assert v1 in graph.in_neighbors([v0, v1])

    # Check out-neighbors
    assert v0 in graph.out_neighbors(v=v0)
    assert v0 not in graph.out_neighbors(v=v1)
    assert v1 in graph.out_neighbors(v=v0)
    assert v1 in graph.out_neighbors(v=v1)

    assert v0 in graph.out_neighbors([v0, v1])
    assert v1 in graph.out_neighbors([v0, v1])

    # Check in-edges
    assert e00 in graph.in_edges(v=v0)
    assert e01 in graph.in_edges(v=v1)
    assert e11 in graph.in_edges(v=v1)

    assert e00 in graph.in_edges([v0, v1])
    assert e01 in graph.in_edges([v0, v1])
    assert e11 in graph.in_edges([v0, v1])

    # Check out-edges
    assert e00 in graph.out_edges(v=v0)
    assert e01 in graph.out_edges(v=v0)
    assert e11 in graph.out_edges(v=v1)

    assert e00 in graph.out_edges([v0, v1])
    assert e01 in graph.out_edges([v0, v1])
    assert e11 in graph.out_edges([v0, v1])

    with pytest.raises(AssertionError):
        graph.in_edges(10)

    with pytest.raises(AssertionError):
        graph.out_edges(10)

    with pytest.raises(AssertionError):
        graph.in_neighbors(10)

    with pytest.raises(AssertionError):
        graph.out_neighbors(10)

    with pytest.raises(AssertionError):
        graph.in_edges([10, v0])

    with pytest.raises(AssertionError):
        graph.out_edges([10, v0])

    with pytest.raises(AssertionError):
        graph.in_neighbors([10, v0])

    with pytest.raises(AssertionError):
        graph.out_neighbors([10, v0])


@pytest.mark.skip("Not Implemented")
def test_prune():
    pass


def test_save():
    graph = Graph()
    v1 = graph.Vertex()
    v2 = graph.Vertex()
    v3 = graph.Vertex()
    e = graph.Edge(v1, v2)

    graph.add_vertex(v1)
    graph.add_vertex(v2)
    graph.add_vertex(v3)
    graph.add_edge(e)

    fname = 'test_1'
    graph.save(fname)


def test_derived_class_instantiation_1():
    """
    This test tests whether the necessary functionality
    to be provided by Graph class holds for derived classes.
    """

    # Define a class without overriding Vertex, Edge Classes.
    class ChildGraph(Graph):
        pass

    graph = ChildGraph()
    assert issubclass(graph.vtype, ChildGraph.Vertex)
    assert issubclass(graph.etype, ChildGraph.Edge)


def test_derived_class_instantiation_2():
    """
    This test tests whether the necessary functionality
    to be provided by Graph class holds for derived classes.
    """

    # Define a class overriding Vertex Class, but not Edge Class
    class ChildGraph(Graph):
        class Vertex(Graph.Vertex):
            pass

    graph = ChildGraph()
    assert issubclass(graph.vtype, ChildGraph.Vertex)
    assert issubclass(graph.etype, ChildGraph.Edge)


def test_derived_class_instantiation_3():
    """
    This test tests whether the necessary functionality
    to be provided by Graph class holds for derived classes.
    """

    # Define a class overriding Edge Class, but not Vertex Class
    class ChildGraph(Graph):
        class Edge(Graph.Edge):
            pass

    graph = ChildGraph()
    assert issubclass(graph.vtype, ChildGraph.Vertex)
    assert issubclass(graph.etype, ChildGraph.Edge)


def test_derived_class_instantiation_4():
    """
    This test tests whether the necessary functionality
    to be provided by Graph class holds for derived classes.
    """

    # Define a class overriding Vertex Class and Edge Class AND user supplies UserVertex class
    class ChildGraph(Graph):
        class Vertex(Graph.Vertex):
            pass

    class UserVertex(ChildGraph.Vertex):
        pass

    graph = ChildGraph(vtype=UserVertex)
    assert issubclass(graph.vtype, ChildGraph.Vertex)
    assert issubclass(graph.etype, ChildGraph.Edge)

    # Failure case 1: UserVertex is sub class of parent class, but not ChildGraph.
    class UserVertex(Graph.Vertex):
        pass

    with pytest.raises(AssertionError):
        graph = ChildGraph(vtype=UserVertex)

    # Failure case 2: UserVertex is not a sub-class of any Graph class
    class UserVertex():
        pass

    with pytest.raises(AssertionError):
        graph = ChildGraph(vtype=UserVertex)


def test_derived_class_instantiation_5():
    """
    This test tests whether the necessary functionality
    to be provided by Graph class holds for derived classes.
    """

    # Define a class overriding Vertex Class and Edge Class AND user supplies UserEdge class
    class ChildGraph(Graph):
        class Edge(Graph.Edge):
            pass

    class UserEdge(ChildGraph.Edge):
        pass

    graph = ChildGraph(etype=UserEdge)
    assert issubclass(graph.vtype, ChildGraph.Vertex)
    assert issubclass(graph.etype, ChildGraph.Edge)

    # Failure case 1: UserEdge is sub class of parent class, but not ChildGraph.
    class UserEdge(Graph.Edge):
        pass

    with pytest.raises(AssertionError):
        _ = ChildGraph(etype=UserEdge)

    # Failure case 2: UserVertex is not a sub-class of any Graph class
    class UserEdge:
        pass

    with pytest.raises(AssertionError):
        _ = ChildGraph(etype=UserEdge)


def test_repr():
    graph = Graph()
    assert graph.__str__() == f"Graph(|V|=0 of type=<class 'iglsynth.util.graph.Graph.Vertex'>, " \
        f"|E|=0 of type=<class 'iglsynth.util.graph.Graph.Edge'>)"
