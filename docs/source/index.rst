.. currentmodule:: iglsynth


==================================================================
IGLSynth: Automatic Strategy Synthesis Library
==================================================================

IGLSynth is a high-level Python API for solving Infinite Games and Logic-based strategy Synthesis. It provides
an easy interface to

    1. Define two-player games-on-graphs.
    2. Assign tasks to players using formal logic.
    3. Write solvers to compute winning strategies in the game.

|

IGLSynth consists of 4 modules,

    1. :mod:`~iglsynth.game`: Defines classes representing deterministic/stochastic and concurrent/turn-based games as well as hypergames.
    2. :mod:`~iglsynth.logic`: Defines classes representing formal logic such as Propositional Logic, Linear Temporal Logic etc.
    3. :mod:`~iglsynth.solver`: Defines solvers for different games such as ZielonkaSolver etc.
    4. :mod:`~iglsynth.util`: Defines commonly used classes such as Graph.

|


----------------

Indices and tables
------------------
.. _contents:

.. automodule:: iglsynth

.. toctree::
    :caption: IGLSynth Documentation
    :maxdepth: 2

    Home Page <self>
    Examples <examples>
    API Documentation <api>




Current release and documentation update date:

.. only:: html

    :Release: |version|
    :Date: |today|



* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
