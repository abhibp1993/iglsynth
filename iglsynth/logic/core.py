from abc import ABC
from typing import Callable
from iglsynth.util.graph import *
import iglsynth.util.spot as spot


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
    def __hash__(self):
        raise NotImplementedError

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

        # self._alphabet = None
        self._formula = None
        self._tree = None
        self._eval_func = eval_func

        # Note: It is important to call parse after setting _eval_func.
        #   because "parse" function overrides eval_func if AP name is true/false.
        self.parse(formula)

    def __call__(self, st, *args, **kwargs):
        return self.evaluate(st, args, kwargs)

    def __eq__(self, other):
        assert isinstance(other, ILogic), f"An AP can only be compared with another ILogic formula. " \
            f"Received other={type(other)}"

        return spot.formula(self.formula) == spot.formula(other.formula)

    def __hash__(self):
        return self.formula.__hash__()

    def __repr__(self):
        return f"AP(name={self.formula})"

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def alphabet(self):
        return Alphabet((self,))

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
        if type(other) == PL:
            return PL(f"({self.formula} & {other.formula})")

        raise NotImplementedError(f"AND-ing of AP and {type(other)} is not supported.")

    def _logical_or(self, other):
        if type(other) in (AP, PL):
            return PL(f"({self.formula} | {other.formula})")

        raise NotImplementedError(f"OR-ing of AP and {type(other)} is not supported.")

    def _logical_neg(self):
        return AP(f"(!{self.formula})", eval_func=lambda st, *args, **kwargs: not self._eval_func(st, *args, **kwargs))

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
        assert isinstance(subs_map[self], AP), f"AP can only be substituted by another ILogic formula. " \
            f"Received subs_map[{self}] as obj={subs_map[self]} of type={type(subs_map[self])}"

        return subs_map[self]

    def simplify(self):
        # No simplification possible for an AP.
        pass

    def translate(self):

        # Construct IGLSynth Automaton object from spot_aut
        # Automaton for an AP has same structure for any AP. This is hard-coded here.
        #
        # State 0:
        #   edge(0 -> 0)
        #     label = 1
        #     acc sets = {0}
        # State 1:
        #   edge(1 -> 0)
        #     label = a
        #     acc sets = {}
        #   edge(1 -> 2)
        #     label = !a
        #     acc sets = {}
        # State 2:
        #   edge(2 -> 2)
        #     label = 1
        #     acc sets = {}

        # Create automaton
        igl_aut = Automaton(acc_cond=Automaton.ACC_COSAFE)

        # If AP is either true or false, then automaton has exactly one state.
        if self == AP.TRUE or self == AP.FALSE:
            # Add vertices and mark final vertices
            v0 = Automaton.Vertex(name="0", acc_set=0)
            igl_aut.add_vertex(v0)
            igl_aut.mark_final_st(v0)

            # Add edges
            e00 = Automaton.Edge(u=v0, v=v0, f=self)
            igl_aut.add_edge(e00)

        # Else, construct the above 3-state automaton
        else:
            # Add vertices and mark final vertices
            v0 = Automaton.Vertex(name="0", acc_set=0)
            v1 = Automaton.Vertex(name="1")
            v2 = Automaton.Vertex(name="2")

            igl_aut.add_vertices([v0, v1, v2])
            igl_aut.mark_final_st(v0)

            # Add edges
            e00 = Automaton.Edge(u=v0, v=v0, f=AP("true"))
            e22 = Automaton.Edge(u=v2, v=v2, f=AP("true"))
            e10 = Automaton.Edge(u=v1, v=v0, f=self)
            e12 = Automaton.Edge(u=v1, v=v2,
                                 f=self.__class__(
                                     formula="!"+self.formula,
                                     eval_func=lambda st, *args, **kwargs: not self._eval_func(st, args, kwargs))
                                 )

            igl_aut.add_edges([e00, e10, e12, e22])

        # Return automaton
        return igl_aut

    def is_equivalent(self, other):
        assert isinstance(other, ILogic)
        return spot.formula(self.formula) == spot.formula(other.formula)

    def is_contained_in(self, other):
        assert isinstance(other, ILogic)
        checker = spot.language_containment_checker()
        return checker.contained(spot.formula(self.formula), spot.formula(other.formula))

    def evaluate(self, st, *args, **kwargs):
        if self._eval_func is None:
            raise NotImplementedError

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


class PL(AP):
    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    __hash__ = AP.__hash__

    def __init__(self, formula: str, alphabet: 'Alphabet' = None):
        assert isinstance(formula, str)

        self._alphabet = alphabet
        super(PL, self).__init__(formula=formula, eval_func=None)

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
    def _logical_neg(self):
        return PL(f"(!{self.formula})")

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def parse(self, formula: str):
        # Invoke spot parser
        try:
            spot_formula = spot.formula(formula)
        except SyntaxError:
            raise ParsingError(f"The string {formula} is NOT an acceptable PL formula name.")

        # Check if the formula is propositional logic formula
        mp_class = spot.mp_class(spot_formula)
        if mp_class != "B" and not spot_formula.is_tt() and not spot_formula.is_ff():
            raise ParsingError(f"The string {formula} is NOT an acceptable PL formula.")

        # If input string is acceptable PL formula, then generate syntax tree and update internal variables
        tree = SyntaxTree()
        tree.build_from_spot_formula(spot_formula)

        # Set tree and formula string for PL formula
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
        # Copy the formula into a local variable
        formula = spot.formula(self.formula)

        # For all keys in substitution map, we try replacing self.formula with provided substitutions
        for p in subs_map:

            # Validate type of q. If q is True/False, replace with their logical equivalent.
            q = subs_map[p]
            if q is True:
                q = AP.TRUE

            if q is False:
                q = AP.FALSE

            if not isinstance(p, AP) or not isinstance(q, AP):
                warnings.warn("PL.substitute(...) does not support substitution for non-AP objects. "
                              "The results of substitution may not be correct!")

            spot_p = spot.formula(p.formula)
            spot_q = spot.formula(q.formula)

            formula = formula.substitute(formula=spot_p, new_formula=spot_q)

        return PL(formula=str(formula))

    def simplify(self):
        raise NotImplementedError

    def is_equivalent(self, other):
        assert isinstance(other, ILogic)
        return spot.formula(self.formula) == spot.formula(other.formula)

    def is_contained_in(self, other):
        assert isinstance(other, ILogic)
        checker = spot.language_containment_checker()
        return checker.contained(spot.formula(self.formula), spot.formula(other.formula))

    def evaluate(self, st, *args, **kwargs):
        # Evaluate alphabet to get a substitution map
        subs_map = self.alphabet.evaluate(st, args, kwargs)

        # Substitute valuation of APs in PL formula
        plf = self.substitute(subs_map)

        # Simplify the formula
        spot_formula = spot.formula(plf.formula)
        if spot_formula.is_tt():
            return True
        elif spot_formula.is_ff():
            return False

        raise ValueError(f"Evaluation failed.")


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
        ap_label = dict()
        for p in self:
            ap_label[p] = p(st, args, kwargs)

        return ap_label


class Automaton(Graph):
    """
    Base class for representing automata.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC VARIABLES
    # ------------------------------------------------------------------------------------------------------------------
    # ACC_REACHABILITY = "Reachability"
    ACC_SAFETY = "Safety"
    ACC_COSAFE = "Co-Safety"
    ACC_BUCHI = "Persistence"
    ACC_COBUCHI = "Co-Buchi"

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    class Vertex(Graph.Vertex):
        """
        Base class for representing a vertex of automaton.

        - Two vertices are equal, if they have same names.
        """
        def __init__(self, name, acc_set=-1):
            self._name = name
            self._acc_set = acc_set
            self._is_acc = True if acc_set >= 0 else False

        def __eq__(self, other: 'Automaton.Vertex'):
            return self._name == other._name

        def __hash__(self):
            return self._name.__hash__()

        def __repr__(self):
            return f"Automaton.Vertex(name={self._name}, " \
                f"is_acc={'Yes, acc_set: ' + str(self._acc_set) if self._is_acc else 'No'})"

        @property
        def is_acc(self):
            return self._is_acc

        @property
        def acc_set(self):
            return self._acc_set

    class Edge(Graph.Edge):
        """
        Base class for representing a edge of automaton.

        - :class:`Edge` represents a directed edge.
        - Two edges are equal, if the two :class:`Edge` objects are same.

        :param u: (:class:`Vertex`) Source vertex of edge.
        :param v: (:class:`Vertex`) Target vertex of edge.
        :param f: (:class:`ILogic`) A PL formula over 2^AP denoting the label of edge.
        """

        __hash__ = object.__hash__

        def __init__(self, u: 'Graph.Vertex', v: 'Graph.Vertex', f: 'ILogic'):
            self._source = u
            self._target = v
            self._formula = f

        def __repr__(self):
            return f"Edge(source={self.source}, target={self.target}), f={self.formula}"

        @property
        def source(self):
            """ Returns the source vertex of edge. """
            return self._source

        @property
        def target(self):
            """ Returns the target vertex of edge. """
            return self._target

        @property
        def formula(self):
            return self._formula

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, acc_cond=None, alphabet=None, vtype=None, etype=None, graph=None, file=None):
        assert acc_cond in [self.ACC_BUCHI, self.ACC_COBUCHI, self.ACC_COSAFE, self.ACC_SAFETY]
        assert isinstance(alphabet, Alphabet) or alphabet is None

        super(Automaton, self).__init__(vtype=vtype, etype=etype, graph=graph, file=file)

        self.name = None
        self._acc_condition = acc_cond
        self._alphabet = alphabet
        self._final = dict()            # Map of type {<acc_set_num>: <set: acc_set>}
        self._init_st = None

    def __repr__(self):
        return f"Automaton(|V|={self.num_vertices}, |E|={self.num_edges}, v0={self._init_st}, final={self._final})"

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def acc_cond(self):
        return self._acc_condition

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def init_st(self):
        return self._init_st

    @property
    def final(self):
        if len(self._final) == 1:
            return self._final[0]
        else:
            return self._final.values()

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def initialize(self, init_st):
        assert init_st in self.vertices
        self._init_st = init_st

    def mark_final_st(self, v, acc_set=0):
        assert v in self.vertices

        if acc_set not in self._final:
            self._final[acc_set] = {v}
        else:
            self._final[acc_set].add(v)

    def load_from_hoa_file(self, file):
        raise NotImplementedError

    def load_from_hoa_string(self, string):
        pass


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
MP_CLASS = {"B": "PL",
            "G": "Reachability",
            "S": "Safety",
            "O": "Obligation",
            "P": "Persistence",
            "R": "Recurrence",
            "T": "Reactivity"
            }

TRUE = AP(formula="true", eval_func=lambda st, *args, **kwargs: True)
FALSE = AP(formula="false", eval_func=lambda st, *args, **kwargs: False)
AP.TRUE = TRUE
AP.FALSE = FALSE
