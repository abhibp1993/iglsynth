import pytest
from iglsynth.model.core import *


def test_action_instantiation():
    # Define arbitrary action
    a = Action(name="a", func=lambda x: True)

    # Print action
    assert a.__str__() == "Action(name=a)"
    assert a.__repr__() == "Action(name=a)"
    assert a(None) is True

    # Define action using decorator
    @action
    def a(x):
        return x

    assert a.__str__() == "Action(name=a)"
    assert a.__repr__() == "Action(name=a)"
    assert a(10) == 10

    # Check assertion errors
    with pytest.raises(AssertionError):
        a = Action(name="a", func=True)

    with pytest.raises(AssertionError):
        _ = Action(name="a", func=lambda: True)


