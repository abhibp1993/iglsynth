from iglsynth.logic.ltl import *


def atomic_propositions():
    # ==================================================================================================================
    # Define atomic proposition without evaluation function
    a = AP(formula='a')
    print(a)

    # Define atomic proposition with evaluation function
    @ap
    def is_goal(st):
        return st == 10

    # Define atomic proposition with evaluation function accepting extra arguments
    @ap
    def is_colliding(st, *args):
        obs = args[0]
        return st in obs

    # Define atomic proposition with evaluation function accepting extra keyword arguments
    @ap
    def is_close(st, **kwargs):
        threshold = kwargs['threshold']
        return st - threshold < 10

    # Evaluate above propositions at different states
    print()
    print(is_goal)
    print(f"is_goal(10)={is_goal(10)}")
    print(f"is_goal(20)={is_goal(20)}")

    print()
    print(is_colliding)
    print(f"is_colliding(10, [5, 10])={is_colliding(10, [5, 10])}")
    print(f"is_colliding(20, [5, 10])={is_colliding(20, [5, 10])}")

    print()
    print(is_close)
    print(f"is_close(5, threshold=10)={is_close(5, threshold=10)}")
    print(f"is_close(50, threshold=10)={is_close(50, threshold=10)}")


def propositional_logic_formulas():
    print()

    # A simple PL formula without defining an alphabet.
    plf = PL("a & b")
    print(f"plf={plf}")
    print(f"plf.alphabet={plf.alphabet}")
    print(f"plf(st=10) results in an error, because we haven't "
          f"provided an alphabet with evaluation functions of APs defined")

    # Define alphabet
    @ap
    def a(st, *args, **kwargs):
        return st == 10

    @ap
    def b(st, *args, **kwargs):
        return st in args[0]

    sigma = Alphabet([a, b])

    # Define a propositional logic formula with alphabet
    plf = PL("a & b", alphabet=sigma)
    print(f"plf={plf}")
    print(f"plf.alphabet={plf.alphabet}")
    print(f"plf(st=10)={plf.evaluate(10, [10, 20])}")


def linear_temporal_logic():
    print()
    # Define an LTL formula without giving alphabet
    ltlf = LTL(formula="Gp1 & !(p1 & X(p0 xor p1))")
    print(f"ltlf={ltlf}")

    # Define alphabet
    @ap
    def a(st, *args, **kwargs):
        return st == 10

    @ap
    def b(st, *args, **kwargs):
        return st in args[0]

    sigma = Alphabet([a, b])

    # Define an LTL formula by providing an alphabet
    ltlf = LTL("F(a & Fb)", alphabet=sigma)
    print()
    print(f"ltlf={ltlf}")


if __name__ == '__main__':
    atomic_propositions()
    propositional_logic_formulas()
    linear_temporal_logic()


