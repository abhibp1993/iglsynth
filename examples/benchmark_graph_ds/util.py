"""
Common structure for Vertex and Edge objects for benchmarking.
"""


class Vertex(object):
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return self.name


class Edge(object):
    def __init__(self, u, v):
        self.name = f"({u}, {v})"
        self.source = u
        self.target = v

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return self.name
