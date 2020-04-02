from iglsynth.model.game import *
from iglsynth.solver.zielonka import ZielonkaSolver


def construct_game():

    # Define game
    game = Game(kind=TURN_BASED)

    # Add vertices to game
    vertices = list()
    for i in range(8):
        if i in [0, 4, 6]:
            vertices.append(game.Vertex(name=str(i), turn=1))
        else:
            vertices.append(game.Vertex(name=str(i), turn=2))

    game.add_vertices(vertices)

    # Set the states as final
    v3 = vertices[3]
    v4 = vertices[4]
    game.mark_final(v3)
    game.mark_final(v4)

    # Add edges to the game graph
    edge_list = [(0, 1), (0, 3), (1, 0), (1, 2), (1, 4), (2, 4), (2, 2), (3, 0), (3, 4), (3, 5), (4, 3),
                 (5, 3), (5, 6), (6, 6), (6, 7), (7, 0), (7, 3)]

    for uid, vid in edge_list:
        u = vertices[uid]
        v = vertices[vid]
        game.add_edge(game.Edge(u=u, v=v))

    return game


if __name__ == '__main__':
    # Construct the game
    game = construct_game()

    # Print game, its vertices and its edges
    print(game)
    print()
    for v in game.vertices:
        print(v)

    print()
    for e in game.edges:
        print(e)

    # Zielonka Solver
    solver = ZielonkaSolver(game)
    solver.configure()
    solver.solve()

    # # Print results of running the solver
    print(solver.p1_win)
    print(solver.p2_win)
