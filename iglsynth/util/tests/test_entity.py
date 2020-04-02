import inspect
import iglsynth.util as util


def test_import_util():
    members_util = [m[0] for m in inspect.getmembers(util)]
    assert "Graph" in members_util
    assert "Vertex" in members_util
    assert "Edge" in members_util
    assert "SubGraph" in members_util


def test_equality():
    e1 = util.Entity()
    e2 = util.Entity()
    e3 = util.Entity(name="ent")
    e4 = util.Entity(name="ent")

    assert e1 != e2
    assert e3 == e4


