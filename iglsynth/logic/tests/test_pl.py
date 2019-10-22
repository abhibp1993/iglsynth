import pytest
from iglsynth.logic.core import *


def test_pl_evaluate():

    p = AP("p", lambda st, *args, **kwargs: True)
    q = AP("q", lambda st, *args, **kwargs: False)

    f = p & q
    print(f.evaluate(10))

