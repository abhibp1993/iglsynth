"""
HW Problem 1 for Formal Methods in Robotics.
    Implement the `generate_graph` function for constructing the graph of
    a two-player turn-based gridworld arena.

Instructor: Jie Fu
Author: Abhishek N. Kulkarni
"""

from iglsynth.game.gridworld import *
from itertools import product


########################################################################################################################
# UPDATE THE FOLLOWING FUNCTION ONLY
########################################################################################################################

def generate_graph(self: Gridworld):
    """
    Constructs the graph for two-player turn-based gridworld arena.

    :param self: :class:`Gridworld` object.
    :return: None.
    """
    # Get important attributes of gridworld (for convenience)
    nrows, ncols = self.nrows, self.ncols
    turn = [1, 2]
    conn = self.conn

    # Generate all states: (p1.x, p1.y, p2.x, p2.y, turn)
    coordinates = product(range(nrows), range(ncols), range(nrows), range(ncols), turn)

    # Iterate over all vertices to add edges
    for coord in coordinates:
        # Instantiate a vertex
        u = Gridworld.Vertex(coord=coord)

        # Define actions according to connectivity
        actions = [N, E, S, W]

        if conn == 5 or conn == 9:
            actions.append(STAY)

        if conn > 5:
            actions.extend([NE, NW, SE, SW])

        # Apply actions on vertex to generate neighbors
        neighbors = []
        for act in actions:
            v = act(v=u)
            p1x, p1y, p2x, p2y, _ = v.coordinate
            if 0 <= p1x < nrows and 0 <= p1y < ncols and 0 <= p2x < nrows and 0 <= p2y < ncols:
                neighbors.append(v)

        # Generate edges using neighbors
        edges = [Gridworld.Edge(u=u, v=neighbors[i], act=actions[i]) for i in range(len(neighbors))]

        # Add vertices to graph
        self.add_vertex(u)
        self.add_vertices(neighbors)

        # Add edges to graph
        self.add_edges(edges)


########################################################################################################################
# HELPER DEFINITIONS: DO NOT CHANGE
########################################################################################################################

class Action(object):
    def __init__(self, name=None, func=None):
        assert isinstance(func, Callable), f"Input parameter func must be a function, got {func.__class__}."
        self._name = name
        self._func = func

    def __repr__(self):
        return f"Action({self._name})"

    def __call__(self, v):
        return self._func(v)


def action(func):
    """
    Decorator for creating atomic propositions.
    """
    a = Action(name=func.__name__, func=func)
    return a


@action
def N(v):
    p1x, p1y, p2x, p2y, turn = v.coordinate
    return Gridworld.Vertex(coord=(p1x, p1y + 1, p2x, p2y, 2)) if turn == 1 else \
        Gridworld.Vertex(coord=(p1x, p1y, p2x, p2y + 1, 1))


@action
def E(v):
    p1x, p1y, p2x, p2y, turn = v.coordinate
    return Gridworld.Vertex(coord=(p1x + 1, p1y, p2x, p2y, 2)) if turn == 1 else \
        Gridworld.Vertex(coord=(p1x, p1y, p2x + 1, p2y, 1))


@action
def S(v):
    p1x, p1y, p2x, p2y, turn = v.coordinate
    return Gridworld.Vertex(coord=(p1x, p1y - 1, p2x, p2y, 2)) if turn == 1 else \
        Gridworld.Vertex(coord=(p1x, p1y, p2x, p2y - 1, 1))


@action
def W(v):
    p1x, p1y, p2x, p2y, turn = v.coordinate
    return Gridworld.Vertex(coord=(p1x - 1, p1y, p2x, p2y, 2)) if turn == 1 else \
        Gridworld.Vertex(coord=(p1x, p1y, p2x - 1, p2y, 1))


@action
def NE(v):
    p1x, p1y, p2x, p2y, turn = v.coordinate
    return Gridworld.Vertex(coord=(p1x + 1, p1y + 1, p2x, p2y, 2)) if turn == 1 else \
        Gridworld.Vertex(coord=(p1x, p1y, p2x + 1, p2y + 1, 1))


@action
def NW(v):
    p1x, p1y, p2x, p2y, turn = v.coordinate
    return Gridworld.Vertex(coord=(p1x - 1, p1y + 1, p2x, p2y, 2)) if turn == 1 else \
        Gridworld.Vertex(coord=(p1x, p1y, p2x - 1, p2y + 1, 1))


@action
def SE(v):
    p1x, p1y, p2x, p2y, turn = v.coordinate
    return Gridworld.Vertex(coord=(p1x + 1, p1y - 1, p2x, p2y, 2)) if turn == 1 else \
        Gridworld.Vertex(coord=(p1x, p1y, p2x + 1, p2y - 1, 1))


@action
def SW(v):
    p1x, p1y, p2x, p2y, turn = v.coordinate
    return Gridworld.Vertex(coord=(p1x - 1, p1y - 1, p2x, p2y, 2)) if turn == 1 else \
        Gridworld.Vertex(coord=(p1x, p1y, p2x - 1, p2y - 1, 1))


@action
def STAY(v):
    p1x, p1y, p2x, p2y, turn = v.coordinate
    return Gridworld.Vertex(coord=(p1x, p1y, p2x, p2y, 2)) if turn == 1 else \
        Gridworld.Vertex(coord=(p1x, p1y, p2x, p2y, 1))


ACTIONS = [N, E, S, W, NE, NW, SE, SW, STAY]
Gridworld.ACTIONS = ACTIONS
Gridworld.generate_graph = generate_graph


def test_1x1_world():
    gw = Gridworld(kind=TURN_BASED, dim=(1, 1), conn=4)
    gw.generate_graph()

    assert gw.num_vertices == 2
    assert gw.num_edges == 0


def test_2x2_world():
    # 4-connectivity will have 2 actions at every state
    gw = Gridworld(kind=TURN_BASED, dim=(2, 2), conn=4)
    gw.generate_graph()
    assert gw.num_vertices == 2 * 2 * 2 * 2 * 2
    assert gw.num_edges == gw.num_vertices * 2

    # 8-connectivity will have 3 actions at every state
    gw = Gridworld(kind=TURN_BASED, dim=(2, 2), conn=8)
    gw.generate_graph()
    assert gw.num_vertices == 2 * 2 * 2 * 2 * 2
    assert gw.num_edges == gw.num_vertices * 3

    # 9-connectivity will have 4 actions at every state
    gw = Gridworld(kind=TURN_BASED, dim=(2, 2), conn=9)
    gw.generate_graph()
    assert gw.num_vertices == 2 * 2 * 2 * 2 * 2
    assert gw.num_edges == gw.num_vertices * 4


if __name__ == '__main__':
    test_1x1_world()
