"""
Type 1: Graph Data Structure
Graph = (
            Dict[Vertex: Tuple[Set[InEdges], Set[OutEdges]]],
            Set[Edges]
        )
"""


class Graph(object):
    def __init__(self):
        self._edges = set()
        self._vemap = dict()

    def add_vertex(self, v):
        if not self.has_vertex(v):
            self._vemap[v] = (set(), set())

    def add_edge(self, e):
        u = e.source
        v = e.target

        if self.has_vertex(u) and self.has_vertex(v):
            self._edges.add(e)
            self._vemap[u][1].add(e)
            self._vemap[v][0].add(e)

    def has_vertex(self, v):
        return v in self._vemap
