from spot import *


def substitute(self, formula, new_formula, *args):
    """
    Substitution is only validated for propositional logic formulas.
    It has been implemented for LTL, but is not tested.
    """
    k = self.kind()

    if k in (op_ff, op_tt):
        return self

    elif k in (op_eword, op_ap):
        if self == formula:
            return new_formula

        return self

    elif k in (op_Not, op_X, op_F, op_G, op_Closure,
             op_NegClosure, op_NegClosureMarked):

        if self == formula:
            return new_formula

        f = substitute(self[0], formula, new_formula, *args)
        return formula.unop(k, f)

    elif k in (op_Xor, op_Implies, op_Equiv, op_U, op_R, op_W,
             op_M, op_EConcat, op_EConcatMarked, op_UConcat):

        if self[0] == formula:
            f1 = new_formula
        else:
            f1 = substitute(self[0], formula, new_formula, *args)

        if self[1] == formula:
            f2 = new_formula
        else:
            f2 = substitute(self[1], formula, new_formula, *args)

        return formula.binop(k, f1, f2)

    elif k in (op_Or, op_OrRat, op_And, op_AndRat, op_AndNLM,
             op_Concat, op_Fusion):

        f = []
        for x in self:
            if x == formula:
                tmp = new_formula
            else:
                tmp = substitute(x, formula, new_formula, *args)

            f.append(tmp)

        return formula.multop(k, f)

    elif k in (op_Star, op_FStar):
        ValueError("IGLSynth does not support op_Star and op_FStar operators for substitution.")

    raise ValueError("unknown type of formula")


formula.substitute = substitute
