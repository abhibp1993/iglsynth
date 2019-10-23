import pytest
from iglsynth.logic.core import *


def test_instantiation():
    p = AP("p")
    q = AP("q")
    r = AP("r")

    sigma = Alphabet([p, q])
    sigma.add(r)

    with pytest.raises((TypeError, AssertionError)):
        sigma.add("r")


def test_contains():
    p = AP("p")
    q = AP("q")
    r = AP("r")

    sigma = Alphabet([p, q])

    assert p in sigma
    assert AP("p") in sigma
    assert q in sigma
    assert not r in sigma
    assert not AP("true") in sigma


def test_evaluate():
    p = AP("p", lambda st, *args, **kwargs: True)
    q = AP("q", lambda st, *args, **kwargs: False)

    sigma = Alphabet([p, q])
    evaluation = sigma.evaluate(10)
    assert {p: True, q: False} == evaluation

