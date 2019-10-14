import pytest


@pytest.mark.skip(reason="Not using graph_tool in v0.2.")
def test_graph_tool():
    import graph_tool as gt
    gt.Graph()