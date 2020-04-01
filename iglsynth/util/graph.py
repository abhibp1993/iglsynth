"""
iglsynth: graph.py

License goes here...
"""

from typing import Iterable, Iterator, List, Union
from functools import reduce
import warnings

import iglsynth.util.entity as entity


class Vertex(entity.Entity):
    def __init__(self, name=None):
        super(Vertex, self).__init__(name=name)


class Edge(entity.Entity):
    def __init__(self, u, v, name=None):
        super(Edge, self).__init__(name)

        # Edge data structure
        self._u = u
        self._v = v


class Graph(entity.Entity):
    Vertex = Vertex
    Edge = Edge

    def __init__(self, name=None):
        # Entity constructor
        super(Graph, self).__init__(name=name)

        # Graph data structure
        self._edges = set()
        self._ve_map_in = dict()
        self._ve_map_out = dict()

    def serialize(self, ignores=None):
        nodes = None
        edges = None
        vprop = None
        eprop = None
        gprop = super(Graph, self).serialize(ignores=["_edges", "_ve_map_in", "_ve_map_out"])

        return gprop


if __name__ == '__main__':
    g = Graph(name="MyGraph")
    ser = g.serialize()
    print(ser)
