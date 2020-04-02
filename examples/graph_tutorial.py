import iglsynth.util as util
import iglsynth.readwrite.iglpickle as io
import logging

# Example of how to set up a logger
logging.basicConfig(filename="logs/graph_tutorial.log", level=logging.DEBUG,
                    format='%(levelname)s:%(asctime)s:%(filename)s:%(funcName)s:%(name)s\n\t%(message)s')
logging.info("++++++++++++++++++++++++++++++++++++++++++++")

if __name__ == '__main__':
    # Create a graph
    #   Name, ID are different. When name is not specified, id becomes the identity of graph.
    g1 = util.Graph()
    g2 = util.Graph(name="MyGraph")

    logging.debug("Hello")
    print(g1)
    print(g2)

    # Create a vertices for two graphs
    #   Recommendation: Use graph_obj.Vertex to create new vertices.
    v1 = g1.Vertex()
    v2 = g1.Vertex(name=(10, 20))   # Yes! Names can be python objects!
    v3 = g2.Vertex(name=(10, 20))
    v4 = g2.Vertex(name=(10, 20))

    v5 = util.Vertex()              # It is possible to create vertices like this. But this is discouraged.
    v6 = util.Vertex()

    # Note the two vertices are equal if they have the same name, although they may have different id's.
    print(v1, v2, v3, v4, v5, v6)
    print(f"v1 == v2: {v1 == v2}")
    print(f"v3 == v4: {v3 == v4}")
    print(f"v3.id={v3.id}, v4.id={v4.id}")

    # Create edges
    #   Just like vertices, we recommend creating edges graph_obj.Edge
    e1 = g1.Edge(v1, v2)
    e2 = g2.Edge(v3, v4, name=(v3, v4, "act"))
    e3 = g2.Edge(v3, v4, name=(v3, v4, "fly"))

    # Add vertices and edges to graphs
    g1.add_vertex(v1)
    g1.add_vertex(v2)
    g2.add_vertices([v3, v4, v5, v6])

    g1.add_edge(e1)
    g2.add_edges([e2, e3])

    print(list(g1.vertices), list(g1.edges))
    print(g2.num_vertices, g1.num_edges)
    print(g1, g2)

    # Save the graph
    io.save(g1)     # Name will automatically generated.
    io.save(g2, fname="logs/g2")

    # Load the graph
    g2_load = io.load(fname="logs/g2")
    print(g2_load == g2)
