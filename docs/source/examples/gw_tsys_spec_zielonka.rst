
.. _Example Game Definition By TSys and LTL:

Gridworld Problem: Game on Graph
================================

This example demonstrates how to construct a game on graph using a :class:`Gridworld`
transition system and an :class:`LTL` specification for P1.

In general, there are three ways to define a game on graph, namely

    * By explicitly adding vertices and edges to the graph and marking the accepting states,
    * By providing a transition system and a formal specification,
    * By providing a game field and player objects.

Presently, in IGLSynth v0.2.3, only first two are supported. See :ref:`Example Game Definition By TSys and LTL`
for an example of constructing game on graph by explicitly adding vertices and edges.


Define Transition System
------------------------

To define a game using transition system and P1's specification, first define the transition system.
In general, a transition system may be defined using :class:`TSys` class.
In this example, we use a predefined :class:`Gridworld` transition system from
``iglsynth.game.gridworld`` module::

    from iglsynth.game.gridworld import *

    # Define transition system
    tsys = Gridworld(kind=TURN_BASED, dim=(3, 3), p1_actions=CONN_4, p2_actions=CONN_4)
    tsys.generate_graph()


Define LTL Specification
------------------------

To define P1's objective using an LTL specification, import the logic module::

    from iglsynth.logic.ltl import *


An :class:`LTL` formula is defined over an alphabet. Hence, we start by defining :class:`AP` objects
using which we will construct an alphabet.

In this demo example, we will represent P1's objective to reach to a goal. Such a reachability specification
can be written as :math:`\varphi = \Diamond a` where :math:`a` is an AP representing goal.
So, define the AP as::

    GOAL = (0, 0)
    a = AP("a", lambda st, *args, **kwargs: st.coordinate[0:2] == GOAL)

and the specification as::

    spec = LTL("Fa", alphabet=Alphabet([a]))


Define Game Object
------------------

Given a transition system and specification, we will now define a game.
To define game, we require the game module::

    from iglsynth.game.game import *

Now, instantiate and define a game as follows::

    game = Game(kind=TURN_BASED)
    game.define(tsys, spec)



Solve the Game
--------------

The final step is to invoke a solver to solve the game.
We will use Zielonka's algorithm to solve the above game.
Note that Zielonka's algorithm computes winning region for P1 in a
deterministic two-player zero-sum game.

In IGLSynth, Zielonka's algorithm is implemented in ``zielonka`` module::

    from iglsynth.solver.zielonka import ZielonkaSolver


To run the solver, first instantiate it and call the ``solve`` method::

    solver = ZielonkaSolver(game)
    solver.solve()


The ``solver.solve()`` runs the solver on the ``Game`` object ``game`` that encodes the game on graph.
The solution of solver can be accessed using the properties::

    print(solver.p1_win)
    print(solver.p2_win)

which returns the winning sets for P1 and P2.