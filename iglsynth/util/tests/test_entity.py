import pytest
import inspect
import iglsynth.util as util


def test_import_util():
    members_util = [m[0] for m in inspect.getmembers(util)]
    assert "Graph" in members_util
    assert "Vertex" in members_util
    assert "Edge" in members_util
    assert "SubGraph" in members_util


def test_entity_hashing():
    simple_entity = util.Entity(name="NewEntity")
    assert hash(simple_entity) == hash("NewEntity")


def test_entity_equality():
    e1 = util.Entity()
    e2 = util.Entity()
    e3 = util.Entity(name="ent")
    e4 = util.Entity(name="ent")

    assert e1 != e2
    assert e3 == e4


def test_subclass_entity_without_args():

    class Vertex(util.Entity):
        def __init__(self, name, **kwargs):
            super(Vertex, self).__init__(name, **kwargs)

    v1 = Vertex(name="v1")
    v2 = Vertex("v1")
    v3 = Vertex("v3")

    # Check uniqueness of v1, given name
    assert id(v1) == id(v2)
    assert id(v1) != id(v3)
    assert id(v2) != id(v3)


def test_subclass_entity_with_args():

    class Edge(util.Entity):
        def __init__(self, u, v, **kwargs):
            super(Edge, self).__init__(name=(u, v), **kwargs)

    e1 = Edge(1, 2)
    e2 = Edge(1, 2)
    e3 = Edge(1, 3)

    # Check uniqueness of v1, given name
    assert id(e1) == id(e2)
    assert id(e1) != id(e3)
    assert id(e2) != id(e3)


def test_kwargs_mismatch():
    e1 = util.Entity(name="v1", **{"x": 10, "y": 20})
    e2 = util.Entity(name="v1")
    e3 = util.Entity(name="v1", **{"x": 10})

    assert id(e1) == id(e2)
    assert id(e1) == id(e3)

    with pytest.raises(AssertionError):
        _ = util.Entity(name="v1", **{"x": 10, "y": 30})


