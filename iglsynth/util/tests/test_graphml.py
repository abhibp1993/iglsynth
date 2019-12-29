from iglsynth.util.graphml import *
from iglsynth.util.graph import *
from iglsynth.game.game import *


def test_write_1():
    graph = Graph()
    v1 = graph.Vertex()
    v2 = graph.Vertex()
    e = graph.Edge(v1, v2)

    graph.add_vertex(v1)
    graph.add_vertex(v2)
    graph.add_edge(e)

    fname = 'test_1.graphml'
    parser = GraphMLParser(graph=graph)
    parser.write(fname=fname)


def test_write_2():
    graph = Game(kind=CONCURRENT)
    v1 = graph.Vertex(name=(1, 0))
    v2 = graph.Vertex(name=(2, 0))
    e = graph.Edge(v1, v2)

    graph.add_vertex(v1)
    graph.add_vertex(v2)
    graph.add_edge(e)

    graph.mark_final(v1)

    fname = 'test_2.graphml'
    parser = GraphMLParser(graph=graph)
    parser.write(fname=fname)
