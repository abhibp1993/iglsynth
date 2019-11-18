
.. _Example Define Logic Formulas:

Defining Logic Formulas
=======================

This example demonstrates how to define logic formulas using ``iglsynth.logic`` module.
Presently, IGLSynth defines three classes of logic formulas; namely atomic propositions :class:`AP`,
propositional logic :class:`PL` and linear temporal logic :class:`LTL`.


Atomic Propositions
-------------------

The most common use of logic formulas in IGLSynth is to define certain properties of a game on graph.
Hence, we define atomic propositions to be ``Callable`` objects over states (or vertices) of a graph.

An AP can be defined by providing a name::

    a = AP(formula='a')

However, it is desirable to evaluate an AP at a given state.
This can be achieved by instantiating an AP in the following way::

    # Define atomic proposition with evaluation function
    @ap
    def is_goal(st):
        return st == 10

    # Define atomic proposition with evaluation function accepting extra arguments
    @ap
    def is_colliding(st, *args):
        obs = args[0]
        return st in obs

    # Define atomic proposition with evaluation function accepting extra keyword arguments
    @ap
    def is_close(st, **kwargs):
        threshold = kwargs['threshold']
        return st - threshold < 10


Let us understand the three AP definitions given above.
The first AP, ``is_goal``, accepts a state ``st`` as an input parameter and returns whether ``st == 10`` or not.
It is imperative that an :class:`AP` must return a ``bool``.

In many cases, it is convenient to define a parameterized atomic proposition.
In such cases, the extra parameters can be passed to the AP's evaluation function
as optional arguments ``args`` or optional keyword arguments ``kwargs``.

.. note:: It is strongly recommended that AP's function template to have ``*args, **kwargs`` as parameters.

Given an :class:`AP`, it is possible to evaluate it at a given state::

    res = is_goal(10)
    res = is_goal(20)

    res = is_colliding(10, [5, 10])
    res = is_colliding(20, [5, 10])

    res = is_close(5, threshold=10)
    res = is_close(50, threshold=10)



----------------

Propositional Logic Formulas
----------------------------

Propositional Logic Formulas can be defined by instantiating :class:`PL` class.
Similar to :class:`AP`, a propositional logic formula can be defined by passing a formula string
containing only And(``&``), Or(``|``) and/or Negation(``!``) operators::

    plf0 = PL("a & b")
    plf1 = PL("a | b")
    plf2 = PL("!a | b")


A PL formula is, generally, defined over an alphabet.
An alphabet is a set of atomic propositions.
To define a PL formula over alphabet, first define an alphabet::

    @ap
    def a(st, *args, **kwargs):
        return st == 10

    @ap
    def b(st, *args, **kwargs):
        return st in args[0]

    sigma = Alphabet([a, b])

An important feature of alphabet is that it can be evaluated at a given state.
For example,::

    result = sigma.evaluate(10, [10, 20])


returns a dictionary with keys as AP's in alphabet and values as the result
of evaluating the AP at given state. In above case, ``result = {a: True, b: True}``.

.. note:: Observe that evaluating an alphabet at a state is equivalent to computing the label
    of that state.


Now, we can define a PL formula over an alphabet. ::

    plf = PL("a & b", alphabet=sigma)

PL formulas can also be evaluated at a given state. ::

    # PL is callable class
    res = plf(10, [10, 20])

    # Explicitly call evaluate function
    res = plf.evaluate(10, [10, 20])

When a PL formula is evaluated at a given state, the alphabet is evaluated at that state. Then,
the APs in PL formula are substituted with the evaluated values to get back ``True`` or ``False``.

.. warning:: Calling ``PL`` object like ``res = plf(10, [10, 20])`` is currently failing.
    See `Bug Report Issue #17 <https://github.com/abhibp1993/iglsynth/issues/17>`_.

----------------

Temporal Logic Formulas
-----------------------


(Linear) Temporal Logic formulas can be defined by instantiating :class:`LTL` class.
Similar to :class:`PL`, LTL formulas can be defined with/without providing an alphabet. ::

    # Alphabet not provided.
    ltlf0 = LTL(formula="Gp1 & !(p1 & X(p0 xor p1))")

    # Alphabet provided
    ltlf = LTL("F(a & Fb)", alphabet=sigma)

