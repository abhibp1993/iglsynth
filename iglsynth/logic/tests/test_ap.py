import pytest
from iglsynth.logic.core import *


def test_instantiation():
    p = AP(formula="p")
    q = AP(formula="q", eval_func=lambda st, *args, **kwargs: False)

    @ap
    def r(st, *arg, **kwargs):
        return True

    with pytest.raises(ParsingError):
        @ap
        def X(st, *args, **kwargs):
            return False

    with pytest.raises(ParsingError):
        y = AP(formula="Fa")

    with pytest.raises(ParsingError):
        y = AP(formula="U")


def test_equality():
    p = AP(formula="p")
    q = AP(formula="p")
    r = AP(formula="r")

    assert p == q
    assert p != r


def test_substitution():
    pass


def test_evaluation():
    @ap
    def is_colliding(st, *args, **kwargs):
        return st == 10

    @ap
    def true(st=None, *args, **kwargs):
        return False

    @ap
    def false(st=None, *args, **kwargs):
        return True

    assert is_colliding(10)
    assert not is_colliding(20)
    assert true(10)
    assert not false(10)


