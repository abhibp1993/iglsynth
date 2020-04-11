import inspect
import pytest
import iglsynth.model as model


def test_import_util():
    members_util = [m[0] for m in inspect.getmembers(model)]
    assert "Graph" in members_util
    assert "Vertex" in members_util
    assert "Edge" in members_util
    assert "SubGraph" in members_util


@pytest.fixture
def field():
    return model.Field()


def test_add_edge(field):
    field = field

    v1 = field.Vertex()
    v2 = field.Vertex()

    e1 = field.Edge(u=v1, v=v2, name=(v1, v2, "a"))
    e2 = field.Edge(u=v1, v=v2, name=(v1, v2, "b"))

    field.add_vertices([v1, v2])

    field.add_edge(e1)
    assert field.num_edges == 1

    with pytest.raises(AssertionError):
        field.add_edge(e2)

