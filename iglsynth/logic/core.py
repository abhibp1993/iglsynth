import spot
from abc import ABC
from typing import Callable
from iglsynth.util.graph import *


########################################################################################################################
# INTERFACE CLASSES
########################################################################################################################

class ILogic(ABC):
    """
    Interface class to define logic classes.
    """
    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __and__(self, other):
        return self._logical_and(other)

    def __or__(self, other):
        return self._logical_or(other)

    def __neg__(self):
        return self._logical_neg()

    __iand__ = __rand__ = __and__
    __ior__ = __ror__ = __or__
    __invert__ = __neg__

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def alphabet(self):
        raise NotImplementedError

    @property
    def formula(self):
        raise NotImplementedError

    @property
    def size(self):
        raise NotImplementedError

    @property
    def tree(self):
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def _logical_and(self, other):
        raise NotImplementedError

    def _logical_or(self, other):
        raise NotImplementedError

    def _logical_neg(self):
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def parse(self, formula: str):
        raise NotImplementedError

    def substitute(self, subs_map: dict):
        raise NotImplementedError

    def simplify(self):
        raise NotImplementedError

    def translate(self):
        raise NotImplementedError

    def is_equivalent(self, other):
        raise NotImplementedError

    def is_contained_in(self, other):
        raise NotImplementedError


########################################################################################################################
# PRIVATE CLASSES
########################################################################################################################

class SyntaxTree(Graph):

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    class Vertex(Graph.Vertex):
        def __init__(self, spot_formula):
            super(SyntaxTree.Vertex, self).__init__()

            self._formula = str(spot_formula)
            self._node_type = _SPOT_OP_MAP[spot_formula.kind()]

        def __eq__(self, other):
            return spot.formula(self._formula) == spot.formula(other.formula)

        def __hash__(self):
            return spot.formula(self._formula).__hash__()

        def __repr__(self):
            return f"SyntaxTree.Vertex(formula='{self._formula}', kind={self.operator})"

        @property
        def formula(self):
            return self._formula

        @property
        def operator(self):
            return self._node_type

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        super(SyntaxTree, self).__init__(vtype=SyntaxTree.Vertex)
        self._root = None

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def root(self):
        return self._root

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def build_from_spot_formula(self, spot_formula):
        # Start with root of tree
        root = SyntaxTree.Vertex(spot_formula=spot_formula)
        self.add_vertex(root)
        self._root = root

        # Iteratively visit root in spot formula and build a tree in IGLSynth representation.
        stack = [root]
        while len(stack) > 0:
            # Create a vertex for current spot node.
            igl_vertex = stack.pop(0)
            spot_formula = spot.formula(igl_vertex.formula)

            # Get children of spot node and add them to stack.
            for spot_child in spot_formula:
                igl_vertex_child = SyntaxTree.Vertex(spot_formula=spot_child)
                stack.append(igl_vertex_child)


########################################################################################################################
# PUBLIC CLASSES
########################################################################################################################

class AP(ILogic):
    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, formula: str, eval_func: Callable = None):
        assert isinstance(formula, str)

        self._alphabet = None
        self._formula = None
        self._tree = None
        self._eval_func = eval_func

        # Note: It is important to call parse after setting _eval_func.
        #   because "parse" function overrides eval_func if AP name is true/false.
        self.parse(formula)

    def __call__(self, st, *args, **kwargs):
        return self.evaluate(st, args, kwargs)

    def __eq__(self, other):
        res = spot.formula(self.formula) == spot.formula(other.formula)
        return res

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def alphabet(self):
        return Alphabet()

    @property
    def formula(self):
        return self._formula

    @property
    def size(self):
        return 0

    @property
    def tree(self):
        return self._tree

    # ------------------------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def _logical_and(self, other):
        raise NotImplementedError

    def _logical_or(self, other):
        raise NotImplementedError

    def _logical_neg(self):
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def parse(self, formula: str):

        # Invoke spot parser
        try:
            spot_formula = spot.formula(formula)
        except SyntaxError:
            raise ParsingError(f"The string {formula} is NOT an acceptable AP name.")

        # Check if spot recognizes this as an AP
        if not spot_formula.is_literal() and not spot_formula.is_tt() and not spot_formula.is_ff():
            raise ParsingError(f"The string {formula} is NOT an acceptable AP name.")

        # If input string is acceptable AP, then generate syntax tree and update internal variables
        tree = SyntaxTree()
        tree.build_from_spot_formula(spot_formula)

        self._tree = tree
        self._formula = formula

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
        return subs_map[self]

    def simplify(self):
        # No simplification possible for an AP.
        pass

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
        try:
            result = self._eval_func(st, args, kwargs)

            if isinstance(result, bool):
                return result
            else:
                raise ValueError(f"{self.formula}.evaluate(st={st}, args={args}, kwargs={kwargs})"
                                 f"returned {result}, which is not a boolean.")

        except TypeError:
            raise ValueError(f"Given evaluation function does not conform to required signature."
                             f"An evaluation must be:: func(st, *args, **kwargs)")


class Alphabet(set):
    def __init__(self, props=tuple()):
        """ Represents a set of AP objects. """
        assert all(isinstance(p, AP) for p in props)
        super(Alphabet, self).__init__(props)

    def __call__(self, st, *args, **kwargs):
        return self.evaluate(st, args, kwargs)

    def add(self, p: AP):
        assert isinstance(p, AP)
        super(Alphabet, self).add(p)

    def evaluate(self, st, *args, **kwargs):
        return iter(p(st, args, kwargs) for p in self)


########################################################################################################################
# GLOBAL VARIABLES
########################################################################################################################

class ParsingError(Exception):
    """
    Error raised when IGLSynth logic parsing fails.
    """
    pass


def ap(func):
    """
    Decorator for creating atomic propositions.
    """
    p = AP(formula=func.__name__, eval_func=func)
    return p


RESERVED = set()        #: Set of reserved keywords or symbols
_SPOT_OP_MAP = {0: 'ff', 1: 'tt', 3: 'ap', 4: '!',  5: 'X', 6: 'F', 7: 'G', 11: '^',
                12: '->', 13: ' <->', 14: 'U', 21: '|', 23: '&'}
