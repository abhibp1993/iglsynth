import pytest
from iglsynth.util.graph import *


def test_graph_instantiation():
    # 1. Default Constructor
    graph = Graph()

    # 2. Constructor with UserVertex, UserEdge types
    class UserVertex(Graph.Vertex):
        def __init__(self, name):
            self.name = name

    class UserEdge(Graph.Edge):
        def __init__(self, name, u, v):
            super(UserEdge, self).__init__(u, v)
            self.name = name

    graph = Graph(vtype=UserVertex, etype=UserEdge)

    with pytest.raises(AssertionError):
        graph = Graph(vtype=UserEdge, etype=UserVertex)

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


def test_rm_vertex():
    graph = Graph()

    v0 = Graph.Vertex()
    v1 = Graph.Vertex()

    graph.add_vertices([v0, v1])

    graph.rm_vertex(v0)
    assert graph.num_vertices == 1
    assert v0 not in list(graph.vertices)

    graph.rm_vertex(v0)
    assert graph.num_vertices == 1
    assert v0 not in list(graph.vertices)

    graph.rm_vertex(v1)
    assert graph.num_vertices == 0
    assert v0 not in list(graph.vertices)
    assert v1 not in list(graph.vertices)


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

    # Add a new edge between same vertices
    e0 = Graph.Edge(v0, v1)
    graph.add_edge(e0)
    assert graph.num_edges == 2

    # Add edge using UserDefined Edge type
    class UserEdge(Graph.Edge):
        def __init__(self, name, u, v):
            super(UserEdge, self).__init__(u, v)
            self.name = name

    graph = Graph(etype=UserEdge)
    v0 = Graph.Vertex()
    v1 = Graph.Vertex()
    graph.add_vertices([v0, v1])

    graph.add_edge(UserEdge(name="edge", u=v0, v=v1))
    assert graph.num_edges == 1

    with pytest.raises(AssertionError):
        graph.add_edge((0, 1))


@pytest.mark.skip(reason="Removal of Multi-Digraph edge is tricky. Yet to be implemented.")
def test_rm_edge():
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


def test_graph_properties():
    # Create a graph instance
    class UserVertex(Graph.Vertex):
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return self.name

    class UserEdge(Graph.Edge):
        def __init__(self, u, v):
            self.name = f"({u}, {v})"
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

    # TODO Yet to be implemented properties
    # assert graph.vp_names
    # assert graph.ep_names
    # assert graph.gp_names
    # assert graph.is_multigraph


# if __name__ == '__main__':
    # test_graph_instantiation()
    # test_graph_properties()
    # test_add_edges()
    # test_remove_vertices()
    # test_get_set_v_e_g_property()
