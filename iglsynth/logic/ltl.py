from iglsynth.logic.core import *


class LTL(PL):
    """
    Represents an temporal logic formula.

    :param formula: (str) A formula string constructed from

        * Atomic propositions (AP names can be alphanumeric strings
          that are not "true" or "false" (case insensitive) and do
          not contain ``F, G, M, R, U, V, W, X, xor`` as a sub-string.
        * Operators: Negation (!), And(&), Or(|), Eventually(F),
          Always(G), Next(X), Until(U).

    :param alphabet: (:class:`Alphabet`) A set of atomic propositions.

    """

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

    @property
    def mp_class(self):
        """
        Returns the class of LTL formula as per Manna-Pnueli hierarchy.

        :return: (str) A character from {'B', 'S', 'G', 'O', 'R', 'P', 'T'}.

        .. seealso:: A discussion on `Manna-Pnueli Hierarchy <https://spot.lrde.epita.fr/hierarchy.html>`_
        """
        return spot.mp_class(spot.formula(self.formula))

    # ------------------------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def _logical_and(self, other):
        # FIXME: Use parenthesis around sub-formulas.
        return LTL(self.formula + " & " + other.formula)

    def _logical_or(self, other):
        # FIXME: Use parenthesis around sub-formulas.
        return LTL(self.formula + " | " + other.formula)

    def _logical_neg(self):
        # FIXME: Use parenthesis around sub-formulas.
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
        raise NotImplementedError("LTL.substitute is not yet implemented.")

    def simplify(self):
        raise NotImplementedError("LTL.simplify is not yet implemented.")

    def translate(self):

        # Translate LTL formula to spot automaton using spot
        spot_aut = spot.translate(self.formula, "BA", "High", "SBAcc", "Complete")

        num_vertices = spot_aut.num_states()
        init_st = spot_aut.get_init_state_number()

        bdict = spot_aut.get_dict()
        ap_dict = dict()
        for p in spot_aut.ap():
            ap_dict[bdict.varnum(p)] = p

        # Construct IGLSynth.Automaton object from spot automaton
        # Ref: https://spot.lrde.epita.fr/tut21.html
        # Decide the acceptance condition by looking at Manna-Pnueli Hierarchy
        mp_class = self.mp_class
        if mp_class == "B" or mp_class == "G":
            acc_cond = Automaton.ACC_COSAFE
        elif mp_class == "S":
            acc_cond = Automaton.ACC_SAFETY
        elif mp_class == "R":
            acc_cond = Automaton.ACC_BUCHI
        elif mp_class == "P":
            acc_cond = Automaton.ACC_COBUCHI
        else:
            acc_cond = None

        igl_aut = Automaton(acc_cond=acc_cond)
        igl_aut.name = spot_aut.get_name()

        # Add vertices, edges to iglsynth automaton
        for u in range(0, num_vertices):
            source = Automaton.Vertex(name=str(u))
            igl_aut.add_vertex(source)

            is_source_accepting = True
            for e in spot_aut.out(u):
                target = Automaton.Vertex(name=str(e.dst))
                igl_aut.add_vertex(target)

                edge = Automaton.Edge(u=source, v=target, f=spot.bdd_format_formula(bdict, e.cond))
                igl_aut.add_edge(edge)

                # PATCH: e.acc returns a spot-specific mark_t object. I'm not sure how to iterate over these.
                #  Now, the translate function generates a Buchi Automaton, where it is guaranteed that
                #  acceptance set will always be a singleton. Hence, presently we only check if the length
                #  of str(e.acc) is greater than 2; which means there's some acceptance set in e.acc.
                if len(str(e.acc)) <= 2:
                    is_source_accepting = False

            if is_source_accepting:
                igl_aut.mark_final_st(v=source)

        # Set initial state
        igl_aut.initialize(Automaton.Vertex(name=str(init_st)))

        return igl_aut

    # def is_equivalent(self, other):
    #     assert isinstance(other, ILogic)
    #     return spot.formula(self.formula) == spot.formula(other.formula)
    #
    # def is_contained_in(self, other):
    #     assert isinstance(other, ILogic)
    #     checker = spot.language_containment_checker()
    #     return checker.contained(spot.formula(self.formula), spot.formula(other.formula))

    def evaluate(self, st, *args, **kwargs):
        """
        Evaluates the LTL formula over the given state.

        .. warning:: This function is not yet implemented.
        """
        raise NotImplementedError("LTL.evaluate method is not yet implemented.")
