from spot import *


def substitute(self, formula, new_formula, *args):
    """
    Substitutes a sub-formula in spot.formula with another spot.formula.

    :param formula: (spot.formula) Spot formula to be replaced.
    :param new_formula: (spot.formula) Spot formula with which the 'formula' should be replaced with.

    """
    k = self.kind()

    if k in (op_ff, op_tt):
        return self

    elif k in (op_eword, op_ap):
        if self == formula:
            return new_formula

        return self

    elif k in (op_Not, op_X, op_F, op_G):

        if self == formula:
            return new_formula

        f = substitute(self[0], formula, new_formula, *args)
        return formula.unop(k, f)

    # TODO: Add these operators when we add support for LTL substitution.
    # elif k in (op_Xor, op_Implies, op_Equiv, op_U, op_R, op_W, op_M):
    #
    #     if self[0] == formula:
    #         f1 = new_formula
    #     else:
    #         f1 = substitute(self[0], formula, new_formula, *args)
    #
    #     if self[1] == formula:
    #         f2 = new_formula
    #     else:
    #         f2 = substitute(self[1], formula, new_formula, *args)
    #
    #     return formula.binop(k, f1, f2)

    elif k in (op_Or, op_And):

        f = []
        for x in self:
            if x == formula:
                tmp = new_formula
            else:
                tmp = substitute(x, formula, new_formula, *args)

            f.append(tmp)

        return formula.multop(k, f)

    raise ValueError(f"IGLSynth does not support operator of kind={k} for substitution.")


formula.substitute = substitute
