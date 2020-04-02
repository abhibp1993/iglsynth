"""
iglsynth: field.py

License goes here...
"""

import iglsynth.util as util


class Field(util.Graph):
    def add_edge(self, e):
        u = e.source
        v = e.target

        if len(list(self.get_edges(u, v))) > 0:
            self.logger.error(f"Field graph cannot have more than one edge between two vertices.\n"
                              f"\tu={u}, \n"
                              f"\tv={v}, \n"
                              f"\t get_edges(u, v) = {list(self.get_edges(u, v))}")
            raise ValueError(f"Field graph cannot have more than one edge between two vertices.")

        super(Field, self).add_edge(e)


if __name__ == '__main__':
    f = Field()
    v1 = f.Vertex()
    v2 = f.Vertex()
    v3 = f.Vertex()

    e1 = f.Edge(v1, v2, name="e1")
    e2 = f.Edge(v1, v2, name="e2")
    e3 = f.Edge(v2, v3)

    f.add_vertices([v1, v2, v3])
    f.add_edges([e1, e3])
    try:
        f.add_edge(e2)      # Raises error
    except ValueError:
        pass

    f.rm_edge(e1)
    f.add_edge(e2)

