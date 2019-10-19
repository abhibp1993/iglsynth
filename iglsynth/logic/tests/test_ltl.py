from iglsynth.logic.ltl import *


def test_translate():
    # Define a AP; true
    true = LTL(formula="true")
    aut = true.translate()
    assert aut.num_edges == 1
    assert aut.num_vertices == 1
    assert Automaton.Vertex(name="0") in aut.final

    # Define a AP; false
    false = LTL(formula="false")
    aut = false.translate()
    assert aut.num_edges == 1
    assert aut.num_vertices == 1
    assert len(aut.final) == 0

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


