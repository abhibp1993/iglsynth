from iglsynth.game.game import *
from iglsynth.solver.zielonka import ZielonkaSolver

def construct_game():

    # Define game
    game = Game(kind=TURN_BASED)

    # Add vertices to game
    vertices = [game.Vertex(name=str(i)) for i in range(8)]

    for i in [0, 4, 6]:
        vertices[i].turn = 1

    for i in [1, 2, 3, 5, 7]:
        vertices[i].turn = 2

    game.add_vertices(vertices)

    # Add edges to the game graph
    edge_list = [(0, 1), (0, 3), (1, 0), (1, 2), (1, 4), (2, 4), (2, 2), (3, 0), (3, 4), (3, 5), (4, 3),
                 (5, 3), (5, 6), (6, 6), (6, 7), (7, 0), (7, 3)]

    for uid, vid in edge_list:
        u = vertices[uid]
        v = vertices[vid]
        game.add_edge(game.TurnBasedEdge(u=u, v=v))

    return game


if __name__ == '__main__':
    # Construct the game
    game = construct_game()

    # Print game, its vertices and its edges
    print(game)
    for v in game.vertices:
        print(v)

    for e in game.edges:
        print(e)

    # Zielonka Solver
    solver = ZielonkaSolver(game)
    solver.configure(win1=True, win2=True)
    solver.run()

    # Print results of running the solver
    print(solver.win1)
    print(solver.win2)
