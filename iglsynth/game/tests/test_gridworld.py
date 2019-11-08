import pytest
from iglsynth.game.gridworld import *


@pytest.mark.skip("Not yet implemented. ")
def test_instantiation():
    # Simple instantiation
    _ = Gridworld(kind=CONCURRENT, dim=(3, 3), conn=4)
    _ = Gridworld(kind="Concurrent", dim=(3, 3), conn=4)

    # Incorrect kind
    with pytest.raises(AssertionError):
        _ = Gridworld(kind="Random", dim=(3, 3), conn=4)

    # Incorrect connectivity
    with pytest.raises(AssertionError):
        _ = Gridworld(kind=CONCURRENT, dim=(3, 3), conn=2)

    # Incorrect dimensions
    with pytest.raises(AssertionError):
        _ = Gridworld(kind=CONCURRENT, dim=(3.5, 3), conn=4)

    # TODO: Test arena input failures
    # TODO: Test p1 input failures
    # TODO: Test p2 input failures
    # TODO: Test random actions input. They should be ignored. Connectivity should decide the actions.


@pytest.mark.skip("Not yet implemented. ")
def test_generate_graph():
    Vertex = Gridworld.Vertex

    # Create grid world object
    gw = Gridworld(kind=CONCURRENT, dim=(3, 3), conn=4)

    # Initialization cannot be done before graph is initialized.
    with pytest.raises(AssertionError):
        gw.initialize(init_st=Vertex(coord=(0, 0, 0, 0)))

    # Initialize after generating graph
    gw.generate_graph()
    gw.initialize(init_st=Vertex(coord=(0, 0, 0, 0)))

    assert gw.num_vertices == 9 * 9             # A state of grid world is (p1.cell, p2.cell)
    assert gw.num_edges == 24 * 24              # Action is (p1.act, p2.act). We have 1 4-conn, 4 3-conn, 4 2-conn st.



