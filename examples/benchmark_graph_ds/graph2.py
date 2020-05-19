import snap
from bidict import bidict


class Graph(object):
    def __init__(self):
        self.graph = snap.TNEANet.New()
        self.vertices = bidict()
        self.edges = bidict()

    def add_vertex(self, v):
        if not self.has_vertex(v):
            vid = self.graph.AddNode()
            self.vertices[vid] = v

    def add_edge(self, e):
        u = e.source
        v = e.target
        uid = self.vertices.inverse[u]
        vid = self.vertices.inverse[v]

        if self.has_vertex(u) and self.has_vertex(v) and not self.has_edge(e):
            eid = self.graph.AddEdge(uid, vid)
            self.edges[eid] = e

    def has_vertex(self, v):
        if isinstance(v, int):
            return v in self.vertices
        return v in self.vertices.inverse

    def has_edge(self, e):
        if isinstance(e, int):
            return e in self.edges
        return e in self.edges.inverse
