import pytest
from iglsynth.model.field import *

@pytest.mark.skip(reason="Arena module is to be updated to v0.2.")
def test_arena_instantiation():
    # 1. Default Constructor
    arena = Arena()

    # 2. Constructor with UserVertex, UserEdge types
    class UserVertex(Arena.Vertex):
        def __init__(self, name):
            self.name = name

    class UserEdge(Arena.Edge):
        def __init__(self, name, u, v):
            super(UserEdge, self).__init__(u, v)
            self.name = name

    arena = Arena(vtype=UserVertex, etype=UserEdge)

    with pytest.raises(AssertionError):
        arena = Arena(vtype=UserEdge, etype=UserVertex)

    with pytest.raises(AssertionError):
        class UserVertex(Graph.Vertex):
            def __init__(self, name):
                self.name = name

        class UserEdge1(Graph.Edge):
            def __init__(self, name, u, v):
                super(UserEdge1, self).__init__(u, v)
                self.name = name

        arena = Arena(vtype=UserVertex, etype=UserEdge1)

    # 3. Copy Constructor -- TODO
    # graph = Graph(graph=graph)

    # 4. Load Graph -- TODO
    # graph = Graph(file="")
    # graph = Graph(vtype=UserVertex, etype=UserEdge, file="")


@pytest.mark.skip(reason="Arena module is to be updated to v0.2.")
def test_add_edge():
    arena = Arena()
    v0 = Graph.Vertex()
    v1 = Graph.Vertex()
    arena.add_vertices([v0, v1])

    # Add an edge
    e = Arena.Edge(v0, v1)
    arena.add_edge(e)
    assert arena.num_edges == 1

    # Attempt repeat addition of same edge
    arena.add_edge(e)
    assert arena.num_edges == 1

    # Add a new edge between same vertices
    e0 = Arena.Edge(v0, v1)
    arena.add_edge(e0)
    assert arena.num_edges == 1

    # Add edge using UserDefined Edge type
    class GraphEdge(Arena.Edge):
        def __init__(self, name, u, v):
            super(GraphEdge, self).__init__(u, v)
            self.name = name

    class ArenaEdge(Arena.Edge):
        def __init__(self, name, u, v):
            super(ArenaEdge, self).__init__(u, v)
            self.name = name

    arena = Graph(etype=ArenaEdge)
    v0 = Graph.Vertex()
    v1 = Graph.Vertex()
    arena.add_vertices([v0, v1])

    arena.add_edge(ArenaEdge(name="edge", u=v0, v=v1))
    assert arena.num_edges == 1

    with pytest.raises(AssertionError):
        arena.add_edge(GraphEdge(name="graph_edge", u=v0, v=v1))

    with pytest.raises(AssertionError):
        arena.add_edge((0, 1))


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

