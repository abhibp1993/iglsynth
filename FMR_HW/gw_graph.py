"""
HW 1 for Formal Methods in Robotics.
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
    # TODO: Generate the list of call coordinates.
    coordinates = list()

    # Iterate over all vertices to add edges
    for coord in coordinates:
        # Instantiate a vertex
        u = Gridworld.Vertex(coord=coord)

        # Define the actions that must be applied to current state `u`
        #   to generate neighbors of `u`.
        # TODO - Construct the actions list
        actions = list()

        # Apply actions on vertex to generate neighbors.
        # TODO - Construct the neighbors list
        neighbors = list()       # TODO: neighbors is a list of Gridworld.Vertex objects. Populate it in next for-loop
        for act in actions:
            v = None             # Hint: actions are callable, i.e. they act like functions!
            if False:            # TODO: Check whether the new vertex is in the grid world
                neighbors.append(v)

        # TODO: Generate edges (Gridworld.Edge objects) using neighbors
        edges = list()

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
    test_2x2_world()
