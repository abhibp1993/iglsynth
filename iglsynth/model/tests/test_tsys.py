import pytest
from iglsynth.model.tsys import *
from iglsynth.logic.core import *

# Define commonly used variables
a = AP("a")
b = AP("b")
alphabet = Alphabet([a, b])

alpha_1 = Action(name="alpha_1", func=lambda st: True)
alpha_2 = Action(name="alpha_2", func=lambda st: True)
alpha_3 = Action(name="alpha_3", func=lambda st: True)
alpha = [alpha_1, alpha_2, alpha_3]

beta_1 = Action(name="beta_1", func=lambda st: True)
beta_2 = Action(name="beta_2", func=lambda st: True)
beta_3 = Action(name="beta_3", func=lambda st: True)
beta = [beta_1, beta_2, beta_3]


# Turn based TSys with default parameters
def test_initialization_1():
    tsys = TSys(kind=TURN_BASED)
    assert tsys.kind == TURN_BASED


# Concurrent TSys with default parameters
def test_initialization_2():
    tsys = TSys(kind=CONCURRENT)
    assert tsys.kind == CONCURRENT


# [ERROR] TSys with kind as some random string
def test_initialization_3():
    with pytest.raises(AssertionError):
        _ = TSys(kind="Conc")


# [ERROR] TSys with kind as some random non-string
def test_initialization_4():
    with pytest.raises(AssertionError):
        _ = TSys(kind=1)


# Turn based TSys with alphabet, and default actions
def test_initialization_5():
    tsys = TSys(kind=TURN_BASED, alphabet=alphabet)
    assert tsys.kind == TURN_BASED
    assert tsys.alphabet == alphabet


# Concurrent TSys with alphabet, and default actions
def test_initialization_6():
    tsys = TSys(kind=CONCURRENT, alphabet=alphabet)
    assert tsys.kind == CONCURRENT
    assert tsys.alphabet == alphabet


# Turn based TSys p1_actions: given, p2_actions: not given
def test_initialization_7():
    tsys = TSys(kind=TURN_BASED, p1_actions=alpha)
    assert tsys.kind == TURN_BASED
    assert tsys.p1_actions == set(alpha)
    assert tsys.p2_actions == set()


# Turn based TSys p1_actions: not given, p2_actions: given
def test_initialization_8():
    tsys = TSys(kind=TURN_BASED, p2_actions=beta)
    assert tsys.kind == TURN_BASED
    assert tsys.p1_actions == set()
    assert tsys.p2_actions == set(beta)


# Turn based TSys p1_actions: given, p2_actions: given
def test_initialization_9():
    tsys = TSys(kind=TURN_BASED, p1_actions=alpha, p2_actions=beta)
    assert tsys.kind == TURN_BASED
    assert tsys.p1_actions == set(alpha)
    assert tsys.p2_actions == set(beta)


# Concurrent TSys p1_actions: given, p2_actions: not given
def test_initialization_10():
    tsys = TSys(kind=CONCURRENT, p1_actions=alpha)
    assert tsys.kind == CONCURRENT
    assert tsys.p1_actions == set(alpha)
    assert tsys.p2_actions == set()


# Concurrent TSys p1_actions: not given, p2_actions: given
def test_initialization_11():
    tsys = TSys(kind=CONCURRENT, p2_actions=beta)
    assert tsys.kind == CONCURRENT
    assert tsys.p1_actions == set()
    assert tsys.p2_actions == set(beta)


# Concurrent TSys p1_actions: given, p2_actions: given
def test_initialization_12():
    tsys = TSys(kind=CONCURRENT, p1_actions=alpha, p2_actions=beta)
    assert tsys.kind == CONCURRENT
    assert tsys.p1_actions == set(alpha)
    assert tsys.p2_actions == set(beta)


# Turn based TSys:: add vertex (default vtype)
def test_add_vertex_1():
    tsys = TSys(kind=TURN_BASED)

    v1 = tsys.Vertex(name="v1", turn=1)
    v2 = tsys.Vertex(name="v1", turn=1)
    v3 = tsys.Vertex(name="v1", turn=2)
    v4 = tsys.Vertex(name="v4", turn=10)
    v5 = tsys.Vertex(name="v5")

    tsys.add_vertex(v1)
    assert tsys.num_vertices == 1
    assert v1 in tsys.vertices

    tsys.add_vertex(v2)
    assert tsys.num_vertices == 1
    assert v1 in tsys.vertices
    assert v2 in tsys.vertices

    tsys.add_vertex(v3)
    assert tsys.num_vertices == 2
    assert v1 in tsys.vertices
    assert v2 in tsys.vertices
    assert v3 in tsys.vertices

    with pytest.raises(AssertionError):
        tsys.add_vertex(v4)

    with pytest.raises(AssertionError):
        tsys.add_vertex(v5)


# Turn based TSys:: add vertex (custom vtype)
def test_add_vertex_2():
    class UserVertex(TSys.Vertex):
        pass

    tsys = TSys(kind=TURN_BASED, vtype=UserVertex)

    v1 = UserVertex(name="v1", turn=1)
    v2 = UserVertex(name="v1", turn=1)
    v3 = UserVertex(name="v1", turn=2)
    v4 = UserVertex(name="v4", turn=10)
    v5 = UserVertex(name="v5")

    tsys.add_vertex(v1)
    assert tsys.num_vertices == 1
    assert v1 in tsys.vertices

    tsys.add_vertex(v2)
    assert tsys.num_vertices == 1
    assert v1 in tsys.vertices
    assert v2 in tsys.vertices

    tsys.add_vertex(v3)
    assert tsys.num_vertices == 2
    assert v1 in tsys.vertices
    assert v2 in tsys.vertices
    assert v3 in tsys.vertices

    with pytest.raises(AssertionError):
        tsys.add_vertex(v4)

    with pytest.raises(AssertionError):
        tsys.add_vertex(v5)


# Turn based TSys:: add vertex (derived class vtype)
def test_add_vertex_3():
    class DerivedTSys(TSys):
        pass

    tsys = DerivedTSys(kind=TURN_BASED)

    v1 = tsys.Vertex(name="v1", turn=1)
    v2 = tsys.Vertex(name="v1", turn=1)
    v3 = tsys.Vertex(name="v1", turn=2)
    v4 = tsys.Vertex(name="v4", turn=10)
    v5 = tsys.Vertex(name="v5")

    tsys.add_vertex(v1)
    assert tsys.num_vertices == 1
    assert v1 in tsys.vertices

    tsys.add_vertex(v2)
    assert tsys.num_vertices == 1
    assert v1 in tsys.vertices
    assert v2 in tsys.vertices

    tsys.add_vertex(v3)
    assert tsys.num_vertices == 2
    assert v1 in tsys.vertices
    assert v2 in tsys.vertices
    assert v3 in tsys.vertices

    with pytest.raises(AssertionError):
        tsys.add_vertex(v4)

    with pytest.raises(AssertionError):
        tsys.add_vertex(v5)


# Concurrent TSys:: add vertex (default vtype)
def test_add_vertex_4():
    tsys = TSys(kind=CONCURRENT)

    v1 = tsys.Vertex(name="v1")
    v2 = tsys.Vertex(name="v1")
    v3 = tsys.Vertex(name="v3", turn=10)

    tsys.add_vertex(v1)
    assert tsys.num_vertices == 1
    assert v1 in tsys.vertices

    tsys.add_vertex(v2)
    assert tsys.num_vertices == 1
    assert v1 in tsys.vertices
    assert v2 in tsys.vertices

    with pytest.raises(AssertionError):
        tsys.add_vertex(v3)


# Concurrent TSys:: add vertex (custom vtype)
def test_add_vertex_5():
    class UserVertex(TSys.Vertex):
        pass

    tsys = TSys(kind=CONCURRENT, vtype=UserVertex)

    v1 = UserVertex(name="v1")
    v2 = UserVertex(name="v1")
    v3 = UserVertex(name="v3", turn=10)

    tsys.add_vertex(v1)
    assert tsys.num_vertices == 1
    assert v1 in tsys.vertices

    tsys.add_vertex(v2)
    assert tsys.num_vertices == 1
    assert v1 in tsys.vertices
    assert v2 in tsys.vertices

    with pytest.raises(AssertionError):
        tsys.add_vertex(v3)


# Concurrent TSys:: add vertex (derived class vtype)
def test_add_vertex_6():
    class DerivedTSys(TSys):
        pass

    tsys = DerivedTSys(kind=CONCURRENT)

    v1 = tsys.Vertex(name="v1")
    v2 = tsys.Vertex(name="v1")
    v3 = tsys.Vertex(name="v3", turn=10)

    tsys.add_vertex(v1)
    assert tsys.num_vertices == 1
    assert v1 in tsys.vertices

    tsys.add_vertex(v2)
    assert tsys.num_vertices == 1
    assert v1 in tsys.vertices
    assert v2 in tsys.vertices

    with pytest.raises(AssertionError):
        tsys.add_vertex(v3)


# Turn based TSys:: add edge (default vtype)
def test_add_edge_1():
    tsys = TSys(kind=TURN_BASED, p1_actions=alpha, p2_actions=beta)

    v1 = tsys.Vertex(name="v1", turn=1)
    v2 = tsys.Vertex(name="v2", turn=1)
    v3 = tsys.Vertex(name="v3", turn=2)
    v4 = tsys.Vertex(name="v4", turn=2)
    tsys.add_vertices([v1, v2, v3])

    e12_0 = tsys.Edge(v1, v2, alpha_1)
    e12_1 = tsys.Edge(v1, v2, alpha_1)
    e12_2 = tsys.Edge(v1, v2, alpha_2)
    e12_3 = tsys.Edge(v1, v2, beta_1)

    e32_0 = tsys.Edge(v3, v2, beta_1)
    e32_1 = tsys.Edge(v3, v2, alpha_1)
    e32_2 = tsys.Edge(v3, v2, "action")

    e24_1 = tsys.Edge(v2, v4, alpha_1)
    e42_1 = tsys.Edge(v4, v2, beta_1)

    # Assertion checks
    tsys.add_edge(e12_0)
    assert tsys.num_edges == 1
    assert e12_0 in tsys.edges

    tsys.add_edge(e12_1)
    assert tsys.num_edges == 1
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges

    tsys.add_edge(e12_2)
    assert tsys.num_edges == 2
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges
    assert e12_2 in tsys.edges

    tsys.add_edge(e32_0)
    assert tsys.num_edges == 3
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges
    assert e12_2 in tsys.edges
    assert e32_0 in tsys.edges

    with pytest.raises(AssertionError):
        tsys.add_edge(e12_3)

    with pytest.raises(AssertionError):
        tsys.add_edge(e32_1)

    with pytest.raises(AssertionError):
        tsys.add_edge(e32_2)

    with pytest.raises(AssertionError):
        tsys.add_edge(e24_1)

    with pytest.raises(AssertionError):
        tsys.add_edge(e42_1)


# Turn based TSys:: add edge (custom vtype)
def test_add_edge_2():
    class UserEdge(TSys.Edge):
        pass

    tsys = TSys(kind=TURN_BASED, etype=UserEdge, p1_actions=alpha, p2_actions=beta)

    v1 = tsys.Vertex(name="v1", turn=1)
    v2 = tsys.Vertex(name="v2", turn=1)
    v3 = tsys.Vertex(name="v3", turn=2)
    v4 = tsys.Vertex(name="v4", turn=2)
    tsys.add_vertices([v1, v2, v3])

    e12_0 = UserEdge(v1, v2, alpha_1)
    e12_1 = UserEdge(v1, v2, alpha_1)
    e12_2 = UserEdge(v1, v2, alpha_2)
    e12_3 = UserEdge(v1, v2, beta_1)

    e32_0 = UserEdge(v3, v2, beta_1)
    e32_1 = UserEdge(v3, v2, alpha_1)
    e32_2 = UserEdge(v3, v2, "action")

    e24_1 = UserEdge(v2, v4, alpha_1)
    e42_1 = UserEdge(v4, v2, beta_1)

    # Assertion checks
    tsys.add_edge(e12_0)
    assert tsys.num_edges == 1
    assert e12_0 in tsys.edges

    tsys.add_edge(e12_1)
    assert tsys.num_edges == 1
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges

    tsys.add_edge(e12_2)
    assert tsys.num_edges == 2
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges
    assert e12_2 in tsys.edges

    tsys.add_edge(e32_0)
    assert tsys.num_edges == 3
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges
    assert e12_2 in tsys.edges
    assert e32_0 in tsys.edges

    with pytest.raises(AssertionError):
        tsys.add_edge(e12_3)

    with pytest.raises(AssertionError):
        tsys.add_edge(e32_1)

    with pytest.raises(AssertionError):
        tsys.add_edge(e32_2)

    with pytest.raises(AssertionError):
        tsys.add_edge(e24_1)

    with pytest.raises(AssertionError):
        tsys.add_edge(e42_1)


# Turn based TSys:: add edge (derived class vtype)
def test_add_edge_3():
    class DerivedTSys(TSys):
        pass

    tsys = DerivedTSys(kind=TURN_BASED, p1_actions=alpha, p2_actions=beta)

    v1 = tsys.Vertex(name="v1", turn=1)
    v2 = tsys.Vertex(name="v2", turn=1)
    v3 = tsys.Vertex(name="v3", turn=2)
    v4 = tsys.Vertex(name="v4", turn=2)
    tsys.add_vertices([v1, v2, v3])

    e12_0 = tsys.Edge(v1, v2, alpha_1)
    e12_1 = tsys.Edge(v1, v2, alpha_1)
    e12_2 = tsys.Edge(v1, v2, alpha_2)
    e12_3 = tsys.Edge(v1, v2, beta_1)

    e32_0 = tsys.Edge(v3, v2, beta_1)
    e32_1 = tsys.Edge(v3, v2, alpha_1)
    e32_2 = tsys.Edge(v3, v2, "action")

    e24_1 = tsys.Edge(v2, v4, alpha_1)
    e42_1 = tsys.Edge(v4, v2, beta_1)

    # Assertion checks
    tsys.add_edge(e12_0)
    assert tsys.num_edges == 1
    assert e12_0 in tsys.edges

    tsys.add_edge(e12_1)
    assert tsys.num_edges == 1
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges

    tsys.add_edge(e12_2)
    assert tsys.num_edges == 2
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges
    assert e12_2 in tsys.edges

    tsys.add_edge(e32_0)
    assert tsys.num_edges == 3
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges
    assert e12_2 in tsys.edges
    assert e32_0 in tsys.edges

    with pytest.raises(AssertionError):
        tsys.add_edge(e12_3)

    with pytest.raises(AssertionError):
        tsys.add_edge(e32_1)

    with pytest.raises(AssertionError):
        tsys.add_edge(e32_2)

    with pytest.raises(AssertionError):
        tsys.add_edge(e24_1)

    with pytest.raises(AssertionError):
        tsys.add_edge(e42_1)


# Concurrent TSys:: add edge (default vtype)
def test_add_edge_4():
    tsys = TSys(kind=CONCURRENT, p1_actions=alpha, p2_actions=beta)

    v1 = tsys.Vertex(name="v1")
    v2 = tsys.Vertex(name="v2")
    v3 = tsys.Vertex(name="v3")
    v4 = tsys.Vertex(name="v4")
    tsys.add_vertices([v1, v2, v3])

    e12_0 = tsys.Edge(v1, v2, (alpha_1, beta_1))
    e12_1 = tsys.Edge(v1, v2, (alpha_1, beta_1))
    e12_2 = tsys.Edge(v1, v2, (alpha_2, beta_1))
    e12_3 = tsys.Edge(v1, v2, (alpha_1, beta_2))
    e12_4 = tsys.Edge(v1, v2, alpha_1)

    e32_2 = tsys.Edge(v3, v2, "action")
    e24_1 = tsys.Edge(v2, v4, alpha_1)
    e42_1 = tsys.Edge(v4, v2, beta_1)

    # Assertion checks
    tsys.add_edge(e12_0)
    assert tsys.num_edges == 1
    assert e12_0 in tsys.edges

    tsys.add_edge(e12_1)
    assert tsys.num_edges == 1
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges

    tsys.add_edge(e12_2)
    assert tsys.num_edges == 2
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges
    assert e12_2 in tsys.edges

    tsys.add_edge(e12_3)
    assert tsys.num_edges == 3
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges
    assert e12_2 in tsys.edges
    assert e12_3 in tsys.edges

    with pytest.raises(AssertionError):
        tsys.add_edge(e12_4)

    with pytest.raises(AssertionError):
        tsys.add_edge(e32_2)

    with pytest.raises(AssertionError):
        tsys.add_edge(e24_1)

    with pytest.raises(AssertionError):
        tsys.add_edge(e42_1)


# Concurrent TSys:: add edge (custom vtype)
def test_add_edge_5():
    class UserEdge(TSys.Edge):
        pass

    tsys = TSys(kind=CONCURRENT, etype=UserEdge, p1_actions=alpha, p2_actions=beta)

    v1 = tsys.Vertex(name="v1")
    v2 = tsys.Vertex(name="v2")
    v3 = tsys.Vertex(name="v3")
    v4 = tsys.Vertex(name="v4")
    tsys.add_vertices([v1, v2, v3])

    e12_0 = UserEdge(v1, v2, (alpha_1, beta_1))
    e12_1 = UserEdge(v1, v2, (alpha_1, beta_1))
    e12_2 = UserEdge(v1, v2, (alpha_2, beta_1))
    e12_3 = UserEdge(v1, v2, (alpha_1, beta_2))
    e12_4 = UserEdge(v1, v2, alpha_1)

    e32_2 = UserEdge(v3, v2, "action")
    e24_1 = UserEdge(v2, v4, alpha_1)
    e42_1 = UserEdge(v4, v2, beta_1)

    # Assertion checks
    tsys.add_edge(e12_0)
    assert tsys.num_edges == 1
    assert e12_0 in tsys.edges

    tsys.add_edge(e12_1)
    assert tsys.num_edges == 1
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges

    tsys.add_edge(e12_2)
    assert tsys.num_edges == 2
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges
    assert e12_2 in tsys.edges

    tsys.add_edge(e12_3)
    assert tsys.num_edges == 3
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges
    assert e12_2 in tsys.edges
    assert e12_3 in tsys.edges

    with pytest.raises(AssertionError):
        tsys.add_edge(e12_4)

    with pytest.raises(AssertionError):
        tsys.add_edge(e32_2)

    with pytest.raises(AssertionError):
        tsys.add_edge(e24_1)

    with pytest.raises(AssertionError):
        tsys.add_edge(e42_1)


# Concurrent TSys:: add edge (derived class vtype)
def test_add_edge_6():
    class DerivedTSys(TSys):
        pass

    tsys = DerivedTSys(kind=CONCURRENT, p1_actions=alpha, p2_actions=beta)

    v1 = tsys.Vertex(name="v1")
    v2 = tsys.Vertex(name="v2")
    v3 = tsys.Vertex(name="v3")
    v4 = tsys.Vertex(name="v4")
    tsys.add_vertices([v1, v2, v3])

    e12_0 = tsys.Edge(v1, v2, (alpha_1, beta_1))
    e12_1 = tsys.Edge(v1, v2, (alpha_1, beta_1))
    e12_2 = tsys.Edge(v1, v2, (alpha_2, beta_1))
    e12_3 = tsys.Edge(v1, v2, (alpha_1, beta_2))
    e12_4 = tsys.Edge(v1, v2, alpha_1)

    e32_2 = tsys.Edge(v3, v2, "action")
    e24_1 = tsys.Edge(v2, v4, alpha_1)
    e42_1 = tsys.Edge(v4, v2, beta_1)

    # Assertion checks
    tsys.add_edge(e12_0)
    assert tsys.num_edges == 1
    assert e12_0 in tsys.edges

    tsys.add_edge(e12_1)
    assert tsys.num_edges == 1
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges

    tsys.add_edge(e12_2)
    assert tsys.num_edges == 2
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges
    assert e12_2 in tsys.edges

    tsys.add_edge(e12_3)
    assert tsys.num_edges == 3
    assert e12_0 in tsys.edges
    assert e12_1 in tsys.edges
    assert e12_2 in tsys.edges
    assert e12_3 in tsys.edges

    with pytest.raises(AssertionError):
        tsys.add_edge(e12_4)

    with pytest.raises(AssertionError):
        tsys.add_edge(e32_2)

    with pytest.raises(AssertionError):
        tsys.add_edge(e24_1)

    with pytest.raises(AssertionError):
        tsys.add_edge(e42_1)


# Turn based TSys:: initialize
def test_initialize_1():
    tsys = TSys(kind=TURN_BASED)

    v1 = tsys.Vertex(name="v1", turn=1)
    v2 = tsys.Vertex(name="v2", turn=1)
    tsys.add_vertices([v1])

    # Initialize with vertex not added.
    with pytest.raises(AssertionError):
        tsys.initialize(v2)

    # Initialization requires vertex object only
    with pytest.raises(AssertionError):
        tsys.initialize("hello")

    # Initialize with acceptable vertex
    tsys.initialize(v1)
    assert tsys.init_state == {v1}

    # Reinitialization not permitted
    with pytest.raises(AssertionError):
        tsys.initialize(v1)


# Concurrent TSys:: initialize
def test_initialize_2():
    tsys = TSys(kind=CONCURRENT)

    v1 = tsys.Vertex(name="v1")
    v2 = tsys.Vertex(name="v2")
    tsys.add_vertices([v1])

    # Initialize with vertex not added.
    with pytest.raises(AssertionError):
        tsys.initialize(v2)

    # Initialization requires vertex object only
    with pytest.raises(AssertionError):
        tsys.initialize("hello")

    # Initialize with acceptable vertex
    tsys.initialize(v1)
    assert tsys.init_state == {v1}

    # Reinitialization not permitted
    with pytest.raises(AssertionError):
        tsys.initialize(v1)
