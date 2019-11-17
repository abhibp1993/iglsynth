import pytest
spot = pytest.importorskip("iglsynth.util.spot")


def test_import_spot():
    try:
        import spot
        version = spot.version()
        version = version.split(".")
        major = int(version[0])
        minor = int(version[1])

        assert major >= 2
        assert minor >= 8

        return True

    except:
        raise AssertionError("Spot is not imported successfully!!!")


def test_spot_substitute_tt_ff():
    """ Test AP subsitution only. """

    # Define true and false formula
    tt = spot.formula("true")
    ff = spot.formula("false")

    # Try substituting true with true/false (nothing should happen)
    new_f = tt.substitute(formula=tt, new_formula=tt)
    assert new_f == tt

    new_f = tt.substitute(formula=tt, new_formula=ff)
    assert new_f == tt

    new_f = tt.substitute(formula=ff, new_formula=tt)
    assert new_f == tt

    new_f = tt.substitute(formula=ff, new_formula=ff)
    assert new_f == tt

    # Try substituting true with true/false (nothing should happen)
    new_f = ff.substitute(formula=tt, new_formula=tt)
    assert new_f == ff

    new_f = ff.substitute(formula=tt, new_formula=ff)
    assert new_f == ff

    new_f = ff.substitute(formula=ff, new_formula=tt)
    assert new_f == ff

    new_f = ff.substitute(formula=ff, new_formula=ff)
    assert new_f == ff


def test_spot_substitute_ap():
    """ Test AP subsitution only. """

    a = spot.formula("a")
    b = spot.formula("b")
    tt = spot.formula("true")
    ff = spot.formula("false")

    # Substitute a
    new_f = a.substitute(formula=a, new_formula=tt)
    assert new_f == tt

    new_f = a.substitute(formula=a, new_formula=ff)
    assert new_f == ff

    new_f = a.substitute(formula=a, new_formula=a)
    assert new_f == a

    new_f = a.substitute(formula=a, new_formula=b)
    assert new_f == b


def test_spot_substitute_pl():
    """ Test AP subsitution only. """

    a = spot.formula("a")
    b = spot.formula("b")
    tt = spot.formula("true")
    ff = spot.formula("false")

    phi0 = spot.formula("!a")
    phi1 = spot.formula("a & b")

    # Substitute phi0
    new_f = phi0.substitute(formula=a, new_formula=tt)
    assert new_f == ff

    new_f = phi0.substitute(formula=a, new_formula=ff)
    assert new_f == tt

    new_f = phi0.substitute(formula=a, new_formula=b)
    assert new_f == spot.formula("!b")

    new_f = phi0.substitute(formula=phi0, new_formula=b)
    assert new_f == spot.formula("b")

    # Substitute phi1
    new_f = phi1.substitute(formula=a, new_formula=tt)
    assert new_f == spot.formula("b")

    new_f = new_f.substitute(formula=b, new_formula=tt)
    assert new_f == tt

    new_f = phi1.substitute(formula=a, new_formula=ff)
    assert new_f == ff

    # Substitute a with b
    new_f = phi1.substitute(formula=a, new_formula=b)
    assert new_f == spot.formula("b")


def test_spot_substitute_error():
    a = spot.formula("a U b")

    with pytest.raises(ValueError):
        a.substitute(formula=a, new_formula=spot.formula("true"))
