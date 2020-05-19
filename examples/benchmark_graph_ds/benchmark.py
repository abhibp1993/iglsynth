from random import randint
import time
import tracemalloc

from util import Vertex, Edge
import graph1
import graph2


NUM_NODES = int(1e6)
NUM_EDGES = int(1e6)

vertices = [Vertex(name=f"v{i}") for i in range(NUM_NODES)]
edges = [Edge(u=vertices[randint(0, NUM_NODES-1)], v=vertices[randint(0, NUM_NODES-1)]) for i in range(NUM_EDGES)]


def benchmark_graph(test_name, grf):
    tracemalloc.start()
    time_start = time.time()

    print(f"({test_name}) Adding Vertices", end="")
    for v in vertices:
        grf.add_vertex(v)
    time_vertex_add = time.time()
    print(f": Time={time_vertex_add - time_start} seconds")

    print(f"({test_name}) Adding Edges", end="")
    for e in edges:
        grf.add_edge(e)
    time_edge_add = time.time()
    print(f": Time={time_edge_add - time_vertex_add} seconds")

    time_end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"({test_name}) Total Processing Time: {time_end - time_start} seconds")
    print(f"({test_name}) RAM (peak usage): {peak:,d} bytes")
    print()


if __name__ == '__main__':
    # Graph 1
    benchmark_graph("graph1.py", graph1.Graph())
    benchmark_graph("graph2.py", graph2.Graph())
