import iglsynth.readwrite as io
import pickle


def save(obj, fname=None):
    if fname is None:
        fname = io.get_fname(obj)

    ser = io.serialize(obj)
    pickle.dump(obj=ser, file=open(f"{fname}.iglpkl", "wb"))


def load(fname):
    ser = pickle.load(file=open(f"{fname}.iglpkl", "rb"))
    return io.deserialize(ser)


if __name__ == '__main__':
    from iglsynth.util.graph import Graph, Vertex, Edge

    g = Graph(name="MyGraph")
    v1 = Vertex()
    v2 = Vertex()
    e = Edge(u=v1, v=v2)
    g._edges.add(e)

    save(g, fname="tp")
    ser = load("tp")
    print(ser)
