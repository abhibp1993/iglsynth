import pytest
from iglsynth.logic.ltl import *


def test_translate():
    # Define a AP; true
    true = LTL(formula="true")
    aut = true.translate()
    assert aut.num_edges == 1
    assert aut.num_vertices == 1
    assert Automaton.Vertex(name="0") in aut.final
    assert all(isinstance(e.formula, ILogic) for e in aut.edges)

    # Define a AP; false
    false = LTL(formula="false")
    aut = false.translate()
    assert aut.num_edges == 1
    assert aut.num_vertices == 1
    assert len(aut.final) == 0
    assert all(isinstance(e.formula, ILogic) for e in aut.edges)

    # Define a general LTL formula
    # From spot.randaut:: Gp1 & !(p1 & X(p0 xor p1))
    # HOA: v1
    # name: "Gp1 & (!p1 | X((p0 & p1) | (!p0 & !p1)))"
    # States: 4
    # Start: 2
    # AP: 2 "p1" "p0"
    # acc-name: Buchi
    # Acceptance: 1 Inf(0)
    # properties: trans-labels explicit-labels state-acc complete
    # properties: deterministic very-weak
    # --BODY--
    # State: 0
    # [0&1] 1
    # [!0 | !1] 3
    # State: 1 {0}
    # [0] 1
    # [!0] 3
    # State: 2
    # [0] 0
    # [!0] 3
    # State: 3
    # [t] 3
    # --END--
    ltlf = LTL(formula="Gp1 & !(p1 & X(p0 xor p1))")
    aut = ltlf.translate()

    assert aut.num_edges == 7
    assert aut.num_vertices == 4
    print(aut.final)
    assert len(aut.final) == 1
    assert all(isinstance(e.formula, ILogic) for e in aut.edges)


def test_evaluate():

    p = AP("p", lambda st, *args, **kwargs: st <= 10)
    q = AP("q", lambda st, *args, **kwargs: st >= 10)
    f = LTL(formula="p & q", alphabet=Alphabet([p, q]))
    g = LTL(formula="F(p & q)", alphabet=Alphabet([p, q]))

    assert f.evaluate(st=10) is True
    assert f.evaluate(st=9) is False
    assert f.evaluate(st=11) is False

    assert f(st=10) is True
    assert f(st=9) is False
    assert f(st=11) is False

    with pytest.raises(ValueError):
        g.evaluate(st=11)

    with pytest.raises(ValueError):
        g(st=11)


def test_repr():
    f = LTL("F(a & b)")
    assert f.__repr__() == "LTL(formula=F(a & b))"

