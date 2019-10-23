import pytest
from iglsynth.logic.core import *


# @pytest.mark.skip("Still implementing. ")
def test_pl_evaluate():

    p = AP("p", lambda st, *args, **kwargs: st <= 10)
    q = AP("q", lambda st, *args, **kwargs: st >= 10)
    f = PL(formula="p & q", alphabet=Alphabet([p, q]))

    assert f.evaluate(st=10) is True
    assert f.evaluate(st=9) is False
    assert f.evaluate(st=11) is False


