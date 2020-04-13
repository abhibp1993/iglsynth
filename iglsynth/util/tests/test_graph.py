import importlib
import pytest
import iglsynth.util as util


@pytest.fixture
def grf():
    return util.Graph("Graph")


def test_graph_import():
    import iglsynth.util.graph as graph
    from iglsynth.util.graph import Vertex
    from iglsynth.util.graph import Edge
    from iglsynth.util.graph import Graph
    from iglsynth.util.graph import SubGraph


def test_vertex_instantiation_without_kwargs():
    # Case 1: Automatic name assignment
    v = util.Vertex()
    assert v.name is not None

    # Case 2: User provides name
    v = util.Vertex("Vertex")
    assert v.name == "Vertex"

    v = util.Vertex((10, 20))
    assert v.name == (10, 20)


def test_vertex_instantiation_with_kwargs():
    # Case 1: Automatic name assignment
    v = util.Vertex(name=None)
    assert v.name is not None

    # Case 2: User provides name
    v = util.Vertex(name="Vertex")
    assert v.name == "Vertex"

    # Case 3: Keyword arguments apart from signature are provided
    v = util.Vertex(name="Bouncy", x=10, y=20)
    assert v.name == "Bouncy"
    assert v.x == 10
    assert v.y == 20

    v = util.Vertex("Cartoon", x=10, y=20)
    assert v.name == "Cartoon"
    assert v.x == 10
    assert v.y == 20


def test_edge_instantiation_without_kwargs():

    # Create vertices between which we will define an edge
    u = util.Vertex("u")
    v = util.Vertex("v")

    # Case 1: Automatic name assignment
    #   Remark: users cannot assign name to edge without supplying the keyword "name"
    e = util.Edge(u, v)
    assert e.name == (u, v)
    assert e.source == u
    assert e.target == v


def test_edge_instantiation_with_kwargs():
    # Create vertices between which we will define an edge
    u = util.Vertex("u")
    v = util.Vertex("v")

    # Case 1: User defines the name of edge
    e = util.Edge(u, v, name="edge")
    assert e.name == "edge"
    assert e.source == u
    assert e.target == v

    # Case 2: User does not provide name, but provides other keyword arguments
    e = util.Edge(u, v, x=10, y=0)
    assert e.name == (u, v)
    assert e.source == u
    assert e.target == v


def test_graph_instantiation_without_kwargs():
    # Case 1: Automatic name assignment
    g = util.Graph()
    assert g.name is not None

    # Case 2: User provides name
    g = util.Graph("Graph")
    assert g.name == "Graph"

    g = util.Graph((10, 20))
    assert g.name == (10, 20)


def test_graph_instantiation_with_kwargs():
    # Case 1: Automatic name assignment
    g = util.Graph(name=None)
    assert g.name is not None

    # Case 2: User provides name
    g = util.Graph(name="Vertex")
    assert g.name == "Vertex"

    # Case 3: Keyword arguments apart from signature are provided
    g = util.Graph(name="Bouncy", x=10, y=20)
    assert g.name == "Bouncy"
    assert g.x == 10
    assert g.y == 20


def test_graph_add_vertex(grf):
    # Case 1: Add legitimate vertex
    v0 = util.Vertex("v0")
    grf.add_vertex(v0)

    # Case 2: Add non-vertex object
    with pytest.raises(AssertionError):
        grf.add_vertex(10)


def test_graph_add_edge(grf):
    v0 = grf.Vertex("v0")
    v1 = grf.Vertex("v1")
    v2 = grf.Vertex("v2")
    grf.add_vertex(v0)
    grf.add_vertex(v1)

    # Case 1: Add legitimate edge
    e = grf.Edge(v0, v1)
    grf.add_edge(e)

    # Case 2: Add edge whose source/target is not in graph
    with pytest.raises(AssertionError):
        e = grf.Edge(v0, v2)
        grf.add_vertex(e)

    # Case 3: Add edge with non-edge data type
    with pytest.raises(AssertionError):
        grf.add_vertex(10)


def test_graph_rm_vertex(grf):
    v0 = grf.Vertex("v0")
    v1 = grf.Vertex("v1")
    v2 = grf.Vertex("v2")
    grf.add_vertices([v0, v1, v2])

    assert grf.num_vertices == 3
    assert v0 in grf
    assert v1 in grf
    assert v2 in grf

    grf.rm_vertex(v0)
    assert grf.num_vertices == 2
    assert v0 not in grf
    assert v1 in grf
    assert v2 in grf


def test_graph_rm_edge(grf):
    v0 = grf.Vertex("v0")
    v1 = grf.Vertex("v1")
    v2 = grf.Vertex("v2")
    grf.add_vertices([v0, v1, v2])
    grf.add_edges([grf.Edge(v0, v1), grf.Edge(v1, v2), grf.Edge(v2, v1)])

    assert grf.num_edges == 3
    assert grf.Edge(v0, v1) in grf
    assert grf.Edge(v1, v2) in grf
    assert grf.Edge(v2, v1) in grf

    grf.rm_edge(grf.Edge(v0, v1))
    assert grf.num_edges == 2
    assert grf.Edge(v0, v1) not in grf
    assert grf.Edge(v1, v2) in grf
    assert grf.Edge(v2, v1) in grf


def test_graph_neighborhood_functions(grf):
    v0 = grf.Vertex("v0")
    v1 = grf.Vertex("v1")
    v2 = grf.Vertex("v2")

    grf.add_vertices([v0, v1, v2])
    grf.add_edges([grf.Edge(v0, v1), grf.Edge(v1, v2), grf.Edge(v2, v1)])

    # Check in neighbors
    v0_in_neighbor = tuple(grf.in_neighbors(v0))
    v1_in_neighbor = tuple(grf.in_neighbors(v1))
    assert len(v0_in_neighbor) == 0
    assert len(v1_in_neighbor) == 2
    assert v0 in v1_in_neighbor and v2 in v1_in_neighbor

    # Check in edges
    v0_in_edges = tuple(grf.in_edges(v0))
    v1_in_edges = tuple(grf.in_edges(v1))
    assert len(v0_in_edges) == 0
    assert len(v1_in_edges) == 2
    assert grf.Edge(v0, v1) in v1_in_edges and grf.Edge(v2, v1) in v1_in_edges

    # Check out neighbors
    v0_out_neighbor = tuple(grf.out_neighbors(v0))
    assert len(v0_out_neighbor) == 1
    assert v1 in v0_out_neighbor

    # Check out edges
    v0_out_edges = tuple(grf.out_edges(v0))
    assert len(v0_out_edges) == 1
    assert grf.Edge(v0, v1) in v0_out_edges



