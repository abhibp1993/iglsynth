import pytest
from iglsynth.model.gridworld import *


# [ERROR] Instantiate with unacceptable dimension.
def test_instantiation_1():
    with pytest.raises(AssertionError):
        _ = Gridworld(kind=TURN_BASED, dim=(0, 0))

    with pytest.raises(AssertionError):
        _ = Gridworld(kind=CONCURRENT, dim=(0, 0))

    with pytest.raises(AssertionError):
        _ = Gridworld(kind=TURN_BASED, dim=(1, -1))

    with pytest.raises(AssertionError):
        _ = Gridworld(kind=CONCURRENT, dim=(1, -1))


# Instantiate with acceptable dimension, TURN-BASED, actions given.
def test_instantiation_2():
    gw = Gridworld(kind=TURN_BASED, dim=(1, 1), p1_actions=CONN_4, p2_actions=CONN_4)

    assert gw.kind == TURN_BASED
    assert gw.dim == (1, 1)
    assert gw.nrows == 1
    assert gw.ncols == 1


# Instantiate with acceptable dimension, TURN-BASED, actions not given.
def test_instantiation_3():
    gw = Gridworld(kind=TURN_BASED, dim=(1, 1))

    assert gw.kind == TURN_BASED
    assert gw.dim == (1, 1)
    assert gw.nrows == 1
    assert gw.ncols == 1


# Instantiate with acceptable dimension, CONCURRENT, actions given.
def test_instantiation_4():
    gw = Gridworld(kind=CONCURRENT, dim=(1, 1), p1_actions=CONN_4, p2_actions=CONN_4)

    assert gw.kind == CONCURRENT
    assert gw.dim == (1, 1)
    assert gw.nrows == 1
    assert gw.ncols == 1


# Instantiate with acceptable dimension, CONCURRENT, actions not given.
def test_instantiation_5():
    gw = Gridworld(kind=CONCURRENT, dim=(1, 1))

    assert gw.kind == CONCURRENT
    assert gw.dim == (1, 1)
    assert gw.nrows == 1
    assert gw.ncols == 1


# TURN-BASED: Add vertices
def test_add_vertices_turn_based():
    gw = Gridworld(kind=TURN_BASED, dim=(2, 2))

    v1 = gw.Vertex(coordinate=(0, 0, 0, 0), turn=1)
    v2 = gw.Vertex(coordinate=(0, 0, 0, 0), turn=1)
    v3 = gw.Vertex(coordinate=(0, 0, 0, 0), turn=2)

    gw.add_vertex(v1)
    assert gw.num_vertices == 1
    assert v1 in gw.vertices

    gw.add_vertex(v2)
    assert gw.num_vertices == 1
    assert v1 in gw.vertices
    assert v2 in gw.vertices

    gw.add_vertex(v3)
    assert gw.num_vertices == 2
    assert v1 in gw.vertices
    assert v2 in gw.vertices
    assert v3 in gw.vertices


# TURN-BASED: Add vertices
def test_add_vertices_concurrent():
    gw = Gridworld(kind=CONCURRENT, dim=(2, 2))

    v1 = gw.Vertex(coordinate=(0, 0, 0, 0), turn=None)
    v2 = gw.Vertex(coordinate=(0, 0, 0, 0), turn=None)
    v3 = gw.Vertex(coordinate=(0, 0, 0, 1), turn=None)

    gw.add_vertex(v1)
    assert gw.num_vertices == 1
    assert v1 in gw.vertices

    gw.add_vertex(v2)
    assert gw.num_vertices == 1
    assert v1 in gw.vertices
    assert v2 in gw.vertices

    gw.add_vertex(v3)
    assert gw.num_vertices == 2
    assert v1 in gw.vertices
    assert v2 in gw.vertices
    assert v3 in gw.vertices


# TURN-BASED: 1x1 grid test case
def test_generate_turn_based_1x1():
    gw = Gridworld(kind=TURN_BASED, dim=(1, 1), p1_actions=CONN_4, p2_actions=CONN_4)
    gw.generate_graph()
    assert gw.num_vertices == 2
    assert gw.num_edges == 0


# TURN-BASED: 2x2 grid test case
def test_generate_turn_based_2x2():
    gw = Gridworld(kind=TURN_BASED, dim=(2, 2), p1_actions=CONN_4, p2_actions=CONN_4)
    gw.generate_graph()
    assert gw.num_vertices == 2 * 2 * 2 * 2 * 2
    assert gw.num_edges == gw.num_vertices * 2


# TURN-BASED: 3x3 grid test case
def test_generate_turn_based_3x3():
    gw = Gridworld(kind=TURN_BASED, dim=(3, 3), p1_actions=CONN_4, p2_actions=CONN_4)
    gw.generate_graph()
    assert gw.num_vertices == 3 * 3 * 3 * 3 * 2
    assert gw.num_edges == (2 * 4 + 3 * 4 + 4) * 9 * 2


# CONCURRENT: 1x1 grid test case
def test_generate_concurrent_1x1():
    gw = Gridworld(kind=CONCURRENT, dim=(1, 1), p1_actions=CONN_4, p2_actions=CONN_4)
    gw.generate_graph()
    assert gw.num_vertices == 1
    assert gw.num_edges == 0


# CONCURRENT: 2x2 grid test case
def test_generate_concurrent_2x2():
    gw = Gridworld(kind=CONCURRENT, dim=(2, 2), p1_actions=CONN_4, p2_actions=CONN_4)
    gw.generate_graph()
    assert gw.num_vertices == 2 * 2 * 2 * 2
    assert gw.num_edges == gw.num_vertices * (2 * 2)


# CONCURRENT: 3x3 grid test case
def test_generate_concurrent_3x3():
    """
    Combinatorial calculation:
    - n(vertices) = 3 * 3 * 3 * 3
    - For computing n(edges) note that on a 3 x 3 grid, there are
        4 cells with 2 moves possible,
        4 cells with 3 moves possible,
        1 cell with 4 moves possible.

      Hence, consider 9 possible combinations (M, N) of the cell types where P1 and P2 can be.

        (2, 2)  (2, 3), (2, 4)
        (3, 2)  (3, 3), (3, 4)
        (4, 2)  (4, 3), (4, 4)

      At each of these combinations, count the number of joint-actions possible,
      given (P1, P2) are at cell type (M, N)

        (2*4 * 2*4) (2*4 * 3*4) (2*4 * 4*1)
        (3*4 * 2*4) (3*4 * 3*4) (3*4 * 4*1)
        (4*4 * 2*4) (4*4 * 3*4) (4*1 * 4*1)

      Together this adds up to 576.
    """
    gw = Gridworld(kind=CONCURRENT, dim=(3, 3), p1_actions=CONN_4, p2_actions=CONN_4)
    gw.generate_graph()
    assert gw.num_vertices == 3**4
    assert gw.num_edges == 576

