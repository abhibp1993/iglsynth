from iglsynth.game.game import *
from iglsynth.game.gridworld import *
from iglsynth.logic.ltl import *
from iglsynth.solver.zielonka import ZielonkaSolver


def construct_game():

    # Define game
    tsys = Gridworld(kind=TURN_BASED, dim=(3, 3), p1_actions=CONN_4, p2_actions=CONN_4)
    tsys.generate_graph()

    # Define specification
    GOAL = (0, 0)
    a = AP("a", lambda st, *args, **kwargs: st.coordinate[0:2] == GOAL)
    spec = LTL("Fa", alphabet=Alphabet([a]))

    # Define game
    game = Game(kind=TURN_BASED)
    game.define(tsys, spec)

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
