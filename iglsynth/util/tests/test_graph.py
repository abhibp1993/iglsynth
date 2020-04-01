import pytest
import inspect
import iglsynth.util as util


@pytest.fixture
def graph():
    return util.Graph()


@pytest.fixture
def named_graph():
    return util.Graph(name="Hello")


@pytest.fixture
def custom_vertex_graph():
    class NewVertex(util.Vertex):
        def __init__(self, name=None):
            super(NewVertex, self).__init__(name)
            self.new_vertex = 10

    g = util.Graph()
    g.Vertex = NewVertex
    return g


def test_import_graph():
    members_util = [m[0] for m in inspect.getmembers(util)]
    assert "Graph" in members_util
    assert "Vertex" in members_util
    assert "Edge" in members_util
    assert "SubGraph" in members_util


def test_add_vertex(graph):
    graph = graph

    # Using default vertex type
    graph.add_vertex(graph.Vertex())
    assert graph.num_vertices == 1

    # Using user-defined vertex class
    class UserVertex(graph.Vertex):
        pass

    graph.add_vertex(UserVertex())
    assert graph.num_vertices == 2

    # Using an arbitrary class other than Graph.Vertex or its derivative.
    with pytest.raises(AssertionError):
        graph.add_vertex(10)


def test_add_vertices(graph):
    graph = graph

    v0 = graph.Vertex()
    v1 = graph.Vertex()

    graph.add_vertices([v0, v1])

    with pytest.raises(AssertionError):
        graph.add_vertex([v0, 10])


def test_rm_vertex(graph):
    graph = graph

    v0 = graph.Vertex()
    v1 = graph.Vertex()

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


def test_rm_vertices(graph):
    graph = graph

    v0 = graph.Vertex()
    v1 = graph.Vertex()

    graph.add_vertices([v0, v1])

    # Remove one vertex
    graph.rm_vertices([v0, v1])
    assert graph.num_vertices == 0
    assert v0 not in list(graph.vertices)
    assert v1 not in list(graph.vertices)

    with pytest.raises(AssertionError):
        graph.rm_vertex([10, v0])


def test_has_vertex(graph):

    # Default graph class
    graph = graph
    v0 = graph.Vertex()
    v1 = graph.Vertex()
    v2 = graph.Vertex()
    graph.add_vertices([v0, v1])

    assert graph.has_vertex(v0)
    assert graph.has_vertex(v1)
    assert not graph.has_vertex(v2)

    assert v0 in graph
    assert v1 in graph
    assert v2 not in graph

    # Graph class with custom vertex class
    class UserVertex(graph.Vertex):
        def __init__(self, name):
            super(UserVertex, self).__init__(name)

    graph = graph
    graph.Vertex = UserVertex
    v0 = UserVertex(name="v0")
    v1 = UserVertex(name="v1")

    graph.add_vertex(v0)

    assert graph.has_vertex(v0)
    assert not graph.has_vertex(v1)

    assert v0 in graph
    assert v1 not in graph

    # Derived Graph class with custom vertex class
    class NewVertex(util.Vertex):
        def __init__(self, name):
            super(NewVertex, self).__init__(name)

    class NewGraph(util.Graph):
        Vertex = NewVertex

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


def test_add_edge(graph):
    g = graph
    v0 = g.Vertex()
    v1 = g.Vertex()
    g.add_vertices([v0, v1])

    # Add an edge
    e = g.Edge(v0, v1, name=f"({v0}, {v1}, 1)")
    g.add_edge(e)
    assert g.num_edges == 1

    # Attempt repeat addition of same edge
    g.add_edge(e)
    assert g.num_edges == 1

    # Add a new edge between same vertices
    e0 = g.Edge(v0, v1, name=f"({v0}, {v1}, 2)")
    g.add_edge(e0)
    assert g.num_edges == 2

    # # Add edge using UserDefined Edge type
    class UserEdge(util.Graph.Edge):
        def __init__(self, name, u, v):
            super(UserEdge, self).__init__(u, v, name=name)

    with pytest.raises(AssertionError):
        g.add_edge((0, 1))

    with pytest.raises(AssertionError):
        g.add_edge(UserEdge(name="edge", u=v0, v=10))

    with pytest.raises(AssertionError):
        g.add_edge(UserEdge(name="edge", u=10, v=v0))

    with pytest.raises(AssertionError):
        g.add_edge(UserEdge(name="edge", u=90, v=10))


def test_add_edges(graph):
    g = graph
    v0 = graph.Vertex()
    v1 = graph.Vertex()
    g.add_vertices([v0, v1])

    # Add multiple edges
    e0 = graph.Edge(v0, v1)
    e1 = graph.Edge(v0, v0)

    g.add_edges([])
    assert g.num_edges == 0

    g.add_edges([e0])
    assert g.num_edges == 1

    g.add_edges([e0, e1])
    assert g.num_edges == 2

    with pytest.raises(AssertionError):
        g.add_edges((0, 1))

    with pytest.raises(AssertionError):
        g.add_edge(g.Edge(u=v0, v=10))

    with pytest.raises(AssertionError):
        g.add_edge(g.Edge(u=10, v=v0))

    with pytest.raises(AssertionError):
        g.add_edge(g.Edge(u=90, v=10))


def test_rm_edge(graph):
    """
    .. note: rm_edge should never raise a KeyError (while removing some edge
        from vertex-edge-map. If this happens, check add_edge function to ensure
        whether the vertex-edge-map is properly handled or not.
    """
    g = graph

    v0 = graph.Vertex()
    v1 = graph.Vertex()
    g.add_vertices([v0, v1])

    e00 = graph.Edge(v0, v0)
    e01 = graph.Edge(v0, v1)
    e11 = graph.Edge(v1, v1)
    g.add_edges([e00, e01, e11])

    assert g.num_edges == 3

    g.rm_edge(e00)
    assert g.num_edges == 2
    assert e00 not in list(g.edges) and e01 in list(g.edges) and e11 in list(g.edges)

    g.rm_edge(e00)
    assert g.num_edges == 2
    assert e00 not in list(g.edges) and e01 in list(g.edges) and e11 in list(g.edges)

    g.rm_edges([e01, e11])
    assert g.num_edges == 0
    assert e00 not in list(g.edges) and e01 not in list(g.edges) and e11 not in list(g.edges)

    with pytest.raises(AssertionError):
        g.rm_edge(10)


def test_rm_edges(graph):
    """
    .. note: rm_edge should never raise a KeyError (while removing some edge
        from vertex-edge-map. If this happens, check add_edge function to ensure
        whether the vertex-edge-map is properly handled or not.
    """
    g = graph

    v0 = graph.Vertex()
    v1 = graph.Vertex()
    g.add_vertices([v0, v1])

    e00 = graph.Edge(v0, v0)
    e01 = graph.Edge(v0, v1)
    e11 = graph.Edge(v1, v1)
    g.add_edges([e00, e01, e11])

    # Remove edges
    g.rm_edges([e01, e11])
    assert g.num_edges == 1
    assert e00 in list(g.edges) and e01 not in list(g.edges) and e11 not in list(g.edges)


def test_has_edge(graph):

    # Default graph class
    g = graph

    v0 = g.Vertex()
    v1 = g.Vertex()
    v2 = g.Vertex()

    e01 = g.Edge(v0, v1)
    e02 = g.Edge(v0, v2)

    g.add_vertices([v0, v1])
    g.add_edge(e01)

    assert g.has_edge(e01)
    assert not g.has_edge(e02)

    assert e01 in g
    assert e02 not in g

    # Graph class with custom vertex class
    class UserEdge(util.Graph.Edge):
        def __init__(self, name, u, v):
            super(UserEdge, self).__init__(u, v, name=name)

    g = util.Graph()
    g.Edge = UserEdge

    v0 = g.Vertex()
    v1 = g.Vertex()
    v2 = g.Vertex()

    e01 = g.Edge(name="e01", u=v0, v=v1)
    e02 = g.Edge(name="e01", u=v0, v=v2)

    g.add_vertices([v0, v1])
    g.add_edge(e01)

    assert g.has_edge(e01)
    assert g.has_edge(e02)

    assert e01 in g
    assert e02 in g

    # Derived Graph class with custom vertex class
    class NewEdge(util.Graph.Edge):
        def __init__(self, name, u, v):
            super(NewEdge, self).__init__(u, v, name=name)

    class NewGraph(util.Graph):
        Edge = NewEdge

    g = NewGraph()

    v0 = g.Vertex()
    v1 = g.Vertex()
    v2 = g.Vertex()

    e01 = g.Edge("e01", v0, v1)
    e02 = g.Edge("e01", v0, v2)

    g.add_vertices([v0, v1])
    g.add_edge(e01)

    assert g.has_edge(e01)
    assert g.has_edge(e02)

    assert e01 in g
    assert e02 in g

    with pytest.raises(TypeError):
        assert 10 in g


def test_get_edges(graph):

    g = graph

    v0 = g.Vertex()
    v1 = g.Vertex()
    v2 = g.Vertex()
    g.add_vertices([v0, v1])

    e00 = g.Edge(v0, v0)
    e01 = g.Edge(v0, v1)
    e11 = g.Edge(v1, v1, name=(v1, v1, 1))
    e11_2 = graph.Edge(v1, v1, name=(v1, v1, 2))
    g.add_edges([e00, e01, e11, e11_2])

    # Empty edge retrieval
    assert len(list(g.get_edges(v1, v0))) == 0

    # Single edge retrieval
    assert len(list(g.get_edges(v0, v1))) == 1

    # Multi edge retrieval
    assert len(list(g.get_edges(v1, v1))) == 2

    # One or more vertices not in graph
    with pytest.raises(AssertionError):
        assert len(list(g.get_edges(v1, v2))) == 0


def test_graph_properties(graph):
    # Create a graph instance
    class UserVertex(util.Graph.Vertex):
        def __init__(self, name):
            super(UserVertex, self).__init__(name)

        def __repr__(self):
            return self.name

    class UserEdge(util.Graph.Edge):
        def __init__(self, u, v):
            super(UserEdge, self).__init__(u, v, name=f"({u}, {v})")

        def __repr__(self):
            return self.name

    g = graph
    g.Vertex = UserVertex
    g.Edge = UserEdge

    # Add vertices and edges
    v1, v2, v3 = list(map(UserVertex, ['a', 'b', 'c']))
    g.add_vertices([v1, v2, v3])

    e1, e2, e3, e4 = list(map(UserEdge, [v1, v2, v3, v1], [v2, v3, v1, v1]))
    g.add_edges([e1, e2, e3, e4])

    # Test properties
    assert g.num_vertices == 3
    assert g.num_edges == 4
    assert set(g.vertices) == {v1, v2, v3}
    assert set(g.edges) == {e1, e2, e3, e4}


def test_graph_neighbors(graph):

    # Define a graph
    g = graph

    v0 = g.Vertex()
    v1 = g.Vertex()
    g.add_vertices([v0, v1])

    e00 = g.Edge(v0, v0)
    e01 = g.Edge(v0, v1)
    e11 = g.Edge(v1, v1)
    g.add_edges([e00, e01, e11])

    # Check in-neighbors
    assert v0 in g.in_neighbors(v=v0)
    assert v1 not in g.in_neighbors(v=v0)
    assert v1 in g.in_neighbors(v=v1)
    assert v0 in g.in_neighbors(v=v1)

    assert v0 in g.in_neighbors([v0, v1])
    assert v1 in g.in_neighbors([v0, v1])

    # Check out-neighbors
    assert v0 in g.out_neighbors(v=v0)
    assert v0 not in g.out_neighbors(v=v1)
    assert v1 in g.out_neighbors(v=v0)
    assert v1 in g.out_neighbors(v=v1)

    assert v0 in g.out_neighbors([v0, v1])
    assert v1 in g.out_neighbors([v0, v1])

    # Check in-edges
    assert e00 in g.in_edges(v=v0)
    assert e01 in g.in_edges(v=v1)
    assert e11 in g.in_edges(v=v1)

    assert e00 in g.in_edges([v0, v1])
    assert e01 in g.in_edges([v0, v1])
    assert e11 in g.in_edges([v0, v1])

    # Check out-edges
    assert e00 in g.out_edges(v=v0)
    assert e01 in g.out_edges(v=v0)
    assert e11 in g.out_edges(v=v1)

    assert e00 in g.out_edges([v0, v1])
    assert e01 in g.out_edges([v0, v1])
    assert e11 in g.out_edges([v0, v1])

    with pytest.raises(AssertionError):
        g.in_edges(10)

    with pytest.raises(AssertionError):
        g.out_edges(10)

    with pytest.raises(AssertionError):
        g.in_neighbors(10)

    with pytest.raises(AssertionError):
        g.out_neighbors(10)

    with pytest.raises(AssertionError):
        g.in_edges([10, v0])

    with pytest.raises(AssertionError):
        g.out_edges([10, v0])

    with pytest.raises(AssertionError):
        g.in_neighbors([10, v0])

    with pytest.raises(AssertionError):
        g.out_neighbors([10, v0])


