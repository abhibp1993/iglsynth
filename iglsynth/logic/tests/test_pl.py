import pytest
from iglsynth.logic.core import *


def test_pl_evaluate():
    """ Substitute is called from within evaluate. """

    p = AP("p", lambda st, *args, **kwargs: st <= 10)
    q = AP("q", lambda st, *args, **kwargs: st >= 10)
    f = PL(formula="p & q", alphabet=Alphabet([p, q]))

    assert f.evaluate(st=10) is True
    assert f.evaluate(st=9) is False
    assert f.evaluate(st=11) is False

    assert f(st=10) is True
    assert f(st=9) is False
    assert f(st=11) is False


def test_repr():
    f = PL("a & b")
    assert f.__repr__() == "PL(formula=a & b)"


def test_translate():
    # Define an AP
    @ap
    def is_colliding(st, *args, **kwargs):
        return st == 0

    @ap
    def is_close(st, *args, **kwargs):
        return st < 10

    phi = PL(formula="is_colliding & is_close", alphabet=Alphabet([is_close, is_colliding]))
    aut = phi.translate()
    assert aut.num_edges == 4
    assert aut.num_vertices == 3
    assert Automaton.Vertex(name="0") in aut.final

