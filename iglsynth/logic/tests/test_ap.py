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

    with pytest.raises(NotImplementedError):
        p = AP(formula="p")
        p(10)

    with pytest.raises(ValueError):
        p = AP(formula="p", eval_func=lambda st, *args, **kwargs: 10)
        p(10)

    with pytest.raises(ValueError):
        p = AP(formula="p", eval_func=lambda st: 10)
        p(10)


def test_equality():
    p = AP(formula="p")
    q = AP(formula="p")
    r = AP(formula="r")
    s = PL(formula="s")

    assert p == q
    assert p != r
    assert p != s

    with pytest.raises(AssertionError):
        assert p == 10

    with pytest.raises(AssertionError):
        assert p is True


def test_substitution():
    a = AP("a")
    b = AP("b")
    tt = AP("true")
    ff = AP("false")

    # Substitute a
    new_f = a.substitute({a: tt})
    assert new_f == tt

    new_f = a.substitute({a: ff})
    assert new_f == ff

    new_f = a.substitute({a: b})
    assert new_f == b

    with pytest.raises(AssertionError):
        new_f = a.substitute({a: True})
        assert new_f == tt

    with pytest.raises(AssertionError):
        new_f = a.substitute({a: False})
        assert new_f == ff


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

    with pytest.raises(ValueError):
        a = AP(formula="a", eval_func=lambda st: 10)
        a(10)


def test_tree():
    # Every AP has the same tree structure, a single (root) node of kind: 3 (ap).
    p = AP("p")
    true = AP("true")
    false = AP("false")

    tree = p.tree
    print([v for v in tree.vertices])
    assert tree.num_vertices == 1

    tree = true.tree
    print([v for v in tree.vertices])
    assert tree.num_vertices == 1

    tree = false.tree
    print([v for v in tree.vertices])
    assert tree.num_vertices == 1


def test_translate():
    # Define an AP
    @ap
    def is_colliding(st, *args, **kwargs):
        return st == 0

    aut = is_colliding.translate()
    assert aut.num_edges == 4
    assert aut.num_vertices == 3
    assert Automaton.Vertex(name="0") in aut.final

    # Define a AP; true
    true = TRUE
    aut = true.translate()
    assert aut.num_edges == 1
    assert aut.num_vertices == 1
    assert Automaton.Vertex(name="0") in aut.final

    # Define a AP; false
    false = AP.FALSE
    aut = false.translate()
    assert aut.num_edges == 1
    assert aut.num_vertices == 1
    assert Automaton.Vertex(name="0") in aut.final


def test_repr():
    a = AP("a")
    assert a.__repr__() == "AP(formula=a)"
