from iglsynth.util.graph import *
from iglsynth.game.game import *
import pytest


@pytest.mark.skip(reason="Game module is to be updated to v0.2.")
def test_game_basic():
    graph = Graph()
    graph.add_vertex_property(name="is_final", of_type="bool")
    graph.add_edge_property(name="act", of_type="int")

    print(graph.vertex_properties)
    print(graph.edge_properties)
    print(graph.graph_properties)

    game = Game()
    game.define(graph=graph)

    print(game.kind)
    print(type(graph.is_final), graph.is_final)


@pytest.mark.skip(reason="Game module is to be updated to v0.2.")
def test_game_instantiation():
    # TODO: Check edge types for kind=TURN_BASED and kind=CONCURRENT
    # TODO: Check isinstance, issubclass on vtype and etype.
    pass

