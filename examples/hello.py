from iglsynth.game.game import *
from iglsynth.solver import ZielonkaSolver


if __name__ == '__main__':

    # Instantiate graph
    graph = Graph()

    # Add vertices to graph
    vertices = graph.add_vertices(num=8)

    # Add edges to graph
    edge_list = [(0, 1), (0, 3), (1, 0), (1, 2), (1, 4), (2, 4), (2, 2), (3, 0), (3, 4), (3, 5), (4, 3),
                 (5, 3), (5, 6), (6, 6), (6, 7), (7, 0), (7, 3)]
    edges = list(graph.add_edges(edges=edge_list))

    # Create vertex property to maintain set of final vertices
    graph.add_vertex_property(name="is_final", of_type="bool", default=False)

    # Set the value of property for final vertices
    graph.set_vertex_property(name="is_final", vid=3, value=True)
    graph.set_vertex_property(name="is_final", vid=4, value=True)

    # Create a vertex property "turn" to annotate vertices with turn of players
    graph.add_vertex_property(name="turn", of_type="int")

    # Set value of turn property for player 1
    for vid in [0, 4, 6]:
        graph.set_vertex_property(name="turn", vid=vid, value=1)

    # Set value of turn property for player 2
    for vid in [1, 2, 3, 5, 7]:
        graph.set_vertex_property(name="turn", vid=vid, value=2)

    # Create action as an edge property. Let index of action in edge_list be the action label.
    graph.add_edge_property(name="act", of_type="int")

    # Set the value of property for all edges
    for idx in range(len(edge_list)):
        graph.set_edge_property(name="act", edge=edges[idx], value=idx)

    # Instantiate a turn-based game
    game = Game(kind=TURN_BASED)

    # Define the game
    game.define(graph=graph)

    # Instantiate a solver
    solver = ZielonkaSolver(game=game)

    # Configure the solver to only compute winning regions, and not strategies
    solver.configure(win1=True, win2=True)

    # Run the solver
    solver.run()
    print("win 1: ", solver.win1)
