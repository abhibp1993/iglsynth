from iglsynth.game.game import *
import pytest

"""
Programmer's note: 
    * Game class defines hash function over name of Vertex. Hence, no two vertices can have same name.
    * Game class define equality over "name" and "turn".   
    
"""


def test_game_instantiation():
    # TODO: Check edge types for kind=TURN_BASED and kind=CONCURRENT
    # TODO: Check isinstance, issubclass on vtype and etype.

    # Simple instantiation
    game1 = Game(kind=TURN_BASED)
    game2 = Game(kind=CONCURRENT)

    assert game1.kind == TURN_BASED
    assert game2.kind == CONCURRENT

    with pytest.raises(AssertionError):
        _ = Game(kind="conc")

    # Using custom Vertex and Edge
    class GameVertex(Game.Vertex):
        pass

    class GameEdge(Game.Edge):
        pass

    class GraphVertex(Graph.Vertex):
        pass

    class GraphEdge(Graph.Vertex):
        pass

    _ = Game(kind=TURN_BASED, vtype=GameVertex)
    _ = Game(kind=TURN_BASED, etype=GameEdge)
    _ = Game(kind=TURN_BASED, vtype=GameVertex, etype=GameEdge)

    with pytest.raises(AssertionError):
        _ = Game(kind=TURN_BASED, vtype=GraphVertex)

    with pytest.raises(AssertionError):
        _ = Game(kind=TURN_BASED, etype=GraphEdge)

    with pytest.raises(AssertionError):
        _ = Game(kind=TURN_BASED, vtype=GameVertex, etype=GraphEdge)

    with pytest.raises(AssertionError):
        _ = Game(kind=TURN_BASED, vtype=GraphVertex, etype=GameEdge)

    with pytest.raises(AssertionError):
        _ = Game(kind=CONCURRENT, vtype=GraphVertex)

    with pytest.raises(AssertionError):
        _ = Game(kind=CONCURRENT, etype=GraphEdge)

    with pytest.raises(AssertionError):
        _ = Game(kind=CONCURRENT, vtype=GameVertex, etype=GraphEdge)

    with pytest.raises(AssertionError):
        _ = Game(kind=CONCURRENT, vtype=GraphVertex, etype=GameEdge)


def test_add_vertices():

    # Define a turn-based and a concurrent game.
    game1 = Game(kind=TURN_BASED)
    game2 = Game(kind=CONCURRENT)

    # Add vertex to turn-based game
    game1.add_vertex(game1.Vertex(name="v1", turn=1))
    game1.add_vertex(game1.Vertex(name="v2", turn=2))
    game1.add_vertices([game1.Vertex(name="v3", turn=1), game1.Vertex(name="v4", turn=2)])

    with pytest.warns(UserWarning):
        game1.add_vertex(game1.Vertex(name="v1", turn=1))

    with pytest.raises(AssertionError):
        game1.add_vertex(game1.Vertex(name="v5", turn="hello"))

    with pytest.raises(AssertionError):
        game1.add_vertex(game1.Vertex(name="v5"))

    # Add vertex to concurrent game
    game2.add_vertex(game2.Vertex(name="v1"))
    game2.add_vertex(game2.Vertex(name="v2"))
    game2.add_vertices([game2.Vertex(name="v3"), game2.Vertex(name="v4")])

    with pytest.warns(UserWarning):
        game2.add_vertex(game2.Vertex(name="v1"))

    with pytest.raises(AssertionError):
        game2.add_vertex(game2.Vertex(name="v5", turn=1))

    with pytest.raises(AssertionError):
        game2.add_vertex(game2.Vertex(name="v5", turn=True))


def test_add_edges():
    # Define a turn-based game
    game1 = Game(kind=TURN_BASED)
    v11 = game1.Vertex(name="v1", turn=1)
    v12 = game1.Vertex(name="v2", turn=2)
    game1.add_vertices([v11, v12])

    # Turn-based game, actions are None
    e_11_12 = game1.Edge(u=v11, v=v12)
    game1.add_edge(e_11_12)

    # Turn-based game, actions are given
    e_12_11 = game1.Edge(u=v12, v=v11, act=Action(name="a", func=lambda x: True))
    game1.add_edge(e_12_11)

    with pytest.raises(AssertionError):
        e_12_11 = game1.Edge(u=v12, v=v11, act="N")
        game1.add_edge(e_12_11)

    with pytest.raises(AssertionError):
        a1 = Action(name="a1", func=lambda x: True)
        a2 = Action(name="a2", func=lambda x: True)
        e_12_11 = game1.Edge(u=v12, v=v11, act=(a1, a2))
        game1.add_edge(e_12_11)

    # Define a concurrent game
    game2 = Game(kind=CONCURRENT)
    v21 = game2.Vertex(name="v1")
    v22 = game2.Vertex(name="v2")
    game2.add_vertices([v21, v22])

    # Concurrent game, actions are None
    e_21_22 = game2.Edge(u=v21, v=v22)
    game2.add_edge(e_21_22)

    # Concurrent game, actions are given
    a1 = Action(name="a1", func=lambda x: True)
    a2 = Action(name="a2", func=lambda x: True)
    e_21_22 = game2.Edge(u=v22, v=v21, act=(a1, a2))
    e_22_22 = game2.Edge(u=v22, v=v22, act=[a1, a2])
    game2.add_edge(e_21_22)
    game2.add_edge(e_22_22)

    with pytest.raises(AssertionError):
        e_22_22 = game2.Edge(u=v22, v=v22, act="N")
        game2.add_edge(e_22_22)

    with pytest.raises(AssertionError):
        e_22_22 = game2.Edge(u=v22, v=v22, act=a1)
        game2.add_edge(e_22_22)


def test_vertex_equality():
    # Turn-based vertices
    v1 = Game.Vertex(name="a", turn=1)
    v2 = Game.Vertex(name="a", turn=2)
    v3 = Game.Vertex(name="a", turn=1)

    assert v1.__hash__() == v2.__hash__()
    assert v1 != v2
    assert v1 == v3

    # Concurrent vertices
    v1 = Game.Vertex(name="a")
    v2 = Game.Vertex(name="a")
    v3 = Game.Vertex(name="b")

    assert v1.__hash__() == v2.__hash__()
    assert v1 == v2
    assert v1 != v3


def test_edge_equality():

    a1 = Action(name="a1", func=lambda x: True)
    a2 = Action(name="a2", func=lambda x: True)
    a3 = Action(name="a3", func=lambda x: True)

    # Turn-based edges
    v1 = Game.Vertex(name="a", turn=1)
    v2 = Game.Vertex(name="a", turn=2)
    v3 = Game.Vertex(name="a", turn=1)

    e1 = Game.Edge(u=v1, v=v2)
    e2 = Game.Edge(u=v1, v=v2)
    e3 = Game.Edge(u=v1, v=v3)

    e4 = Game.Edge(u=v1, v=v2, act=a1)
    e5 = Game.Edge(u=v1, v=v3, act=a1)
    e6 = Game.Edge(u=v1, v=v3, act=a1)
    e7 = Game.Edge(u=v1, v=v3, act=a2)

    assert e1 == e2
    assert e1 != e3
    assert e4 != e5
    assert e5 == e6
    assert e6 != e7

    # Concurrent vertices
    v1 = Game.Vertex(name="a")
    v2 = Game.Vertex(name="a")
    v3 = Game.Vertex(name="b")

    e1 = Game.Edge(u=v1, v=v2)
    e2 = Game.Edge(u=v1, v=v2)
    e3 = Game.Edge(u=v1, v=v3)

    e4 = Game.Edge(u=v1, v=v2, act=(a1, a2))
    e5 = Game.Edge(u=v1, v=v3, act=(a1, a2))
    e6 = Game.Edge(u=v1, v=v3, act=(a1, a2))
    e7 = Game.Edge(u=v1, v=v3, act=(a1, a3))

    assert e1 == e2
    assert e1 != e3
    assert e4 != e5
    assert e5 == e6
    assert e6 != e7
