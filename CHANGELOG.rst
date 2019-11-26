Release Notes
=============

0.2.4 (Proposed)
-----------------------

* Solver module

    * [Issue #24] Define ``Strategy`` class to represent deterministic and stochastic strategies.

0.2.3 ()
-----------------------

* Bugs


    * [Issue #20] Automaton.Edge now returns an `AP` or `PL` class object for AP, PL, LTL.translate().
    * [Issue #17] Unexpected AssertionError when calling `PL(st=..)` and `LTL(st=..)` is handled resolved.
    * [Issue #16] Bug in the printing PL, LTL objects was resolved.


* Game module

    * [Issue #6] Gridworld class accept ``p1_action`` and ``p2_action`` separately.
    * [Issue #6] Gridworld class defined with basic 4, 5, 8, 9 connectivity.
    * [Issue #23] Implement ``game.define(tsys, spec)`` function.
    * [Issue #4] Defined ``Kripke`` class to support ``TSys`` class. No special properties or functions are
      associated with ``Kripke`` are defined or implemented.
    * [Issue #5] Updated ``TSys`` constructor signature to accept ``p1_action, p2_action`` instead of ``actions``.
      ``TSys.Vertex`` now requires ``name, turn`` parameters. ``turn = None`` represents a concurrent game.
      ``TSys.Edge`` is updated to represent both concurrent and turn-based edges.


* Solver module

    * [Issue #24] ``ZielonkaSolver`` class defined and implemented. The solver computes winning regions only.


* Utilities

    * [Issue #11] Added `has_vertex`, `has_edge`, `get_edges` functionality to `Graph` class.
    

0.2.2 (17 November 2019)
------------------------

* Docker images

    * Updated ``latest`` and ``dev`` docker images on docker hub. The latest image now ships with iglsynth installed.
    * Set up a GitHub - DockerHub webhook. All pushes to master branch will trigger a docker image build.

* Documentation

    * Added two examples:

        - Game graph construction
        - Logic formula definition

    * Added installation instructions.
    * Fixed bugs in documentation.



0.2.1 (16 November 2019)
------------------------

* Game module
    * (core) Action class defined with "@action" decorator.
    * (game) Game class defined to represent Deterministic 2-player Game.

        * Game can be of two kinds: TURN_BASED or CONCURRENT.
        * Game can be defined by constructing the game graph (i.e. using game.add_vertex, game.add_edge functions)

* Logic module
    * (core) ILogic class added as an interface class to define logic classes.
    * (core) SyntaxTree class added to represent abstract syntax tree of an ILogic formula.
    * (core) AP class added to represent atomic propositions.

        * AP can be defined using decorator "@ap".
        * AP.__call__, AP.evaluate methods provide a way to check whether an AP is true/false in a given state.

    * (core) PL class added to represent propositional logic formulas.

        * PL.__call__, PL.evaluate methods provide a way to check whether the formula is true in a given state.
        * PL.substitute provide a way to substitute APs in PL formula with their valuations (True/False) or other APs.

    * (core) Alphabet class added to represent a set of APs.

        * Alphabet.__call__, Alphabet.evaluate methods provide a way to get a label of a state.

    * (ltl) LTL class is defined.

* Util Module
    *  (graph) Graph classes redefined.

        * Defined "Vertex" and "Edge" base classes to define vertex and edge properties.
        * Adding and removing vertices, edges is implemented.
        * Accessing in/out neighbors/edges is implemented.

* Documentation updated.


0.1.0 (07 August 2019)
----------------------

* Game module
    * Base class for writing different types of games is ready.
    * Deterministic 2 player game is partially defined.

* Solver module
    * Base class for writing solvers is partially ready.
    * Zielonka attractor algorithm is implemented. Only a few configurations are supported.

* Utility module
    * Graph class is ready.
    * SubGraph class is ready.

* Examples
    * An example from `EPFL Slides <http://richmodels.epfl.ch/_media/w2_wed_3.pdf>`_ is added.

* First release of IGLSynth
