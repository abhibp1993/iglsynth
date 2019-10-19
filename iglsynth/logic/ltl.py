from iglsynth.logic.core import *


class LTL(PL):
    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    __hash__ = PL.__hash__

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def alphabet(self):
        return self._alphabet

    @property
    def size(self):
        """
        Reference: https://stackoverflow.com/questions/17920304/what-is-the-size-of-an-ltl-formula
        """
        spot_formula = spot.formula(self.formula)
        unabbr_formula = str(spot.unabbreviate(spot_formula, "FGRMWie^"))
        return unabbr_formula.count("U") + unabbr_formula.count("X")

    @property
    def tree(self):
        return self._tree

    # ------------------------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def _logical_and(self, other):
        return LTL(self.formula + " & " + other.formula)

    def _logical_or(self, other):
        return LTL(self.formula + " | " + other.formula)

    def _logical_neg(self):
        return LTL("!" + self.formula)

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def parse(self, formula: str):
        # Invoke spot parser
        try:
            spot_formula = spot.formula(formula)
        except SyntaxError:
            raise ParsingError(f"The string {formula} is NOT an acceptable LTL formula.")

        # If input is acceptable LTL formula, then generate syntax tree and update internal variables
        tree = SyntaxTree()
        tree.build_from_spot_formula(spot_formula)

        # A non-PL formula cannot be evaluated.
        mp_class = spot.mp_class(spot_formula)
        if mp_class is not MP_CLASS["B"]:
            self._eval_func = None

        # Set tree and formula string for LTL formula
        self._tree = tree
        self._formula = formula

        # Update alphabet
        sigma = {AP(str(ap)) for ap in spot.atomic_prop_collect(spot_formula)}
        if self._alphabet is None:
            self._alphabet = Alphabet(sigma)
        else:
            assert sigma.issubset(self._alphabet), f"Input formula contains APs not in alphabet, {self._alphabet}"

        # Special APs: true and false
        if spot_formula.is_tt():
            self._eval_func = lambda st, *args, **kwargs: True

        if spot_formula.is_ff():
            self._eval_func = lambda st, *args, **kwargs: False

    def substitute(self, subs_map: dict):
        """
        Substitutes the current AP with another AP according to given substitution map.

        :param subs_map: (dict[<Logic>: <Logic>]) A substitution map.
        :return: (AP) Substituted AP object.

        :raises KeyError: When subs_map does not contain the AP "self".
        """
        raise NotImplementedError

    def simplify(self):
        raise NotImplementedError

    def translate(self):
        spot_hoa = spot.translate(self.formula, "BA", "SBAcc").to_str('HOA')
        # TODO: Define DFA type.
        #  return DFA.from_hoa(string=spot_hoa)

    def is_equivalent(self, other):
        assert isinstance(other, ILogic)
        return spot.formula(self.formula) == spot.formula(other.formula)

    def is_contained_in(self, other):
        assert isinstance(other, ILogic)
        checker = spot.language_containment_checker()
        return checker.contained(spot.formula(self.formula), spot.formula(other.formula))

    def evaluate(self, st, *args, **kwargs):
        raise NotImplementedError
