"""
iglsynth: kripke.py

License goes here...
"""

from iglsynth.logic.core import *


class Kripke(Graph):
    """
    A graph representing a Kripke structure.

    :param alphabet: (:class:`Alphabet`) A set of atomic propositions defined over the Kripke structure.
    :param vtype: (class) Class representing vertex objects.
    :param etype: (class) Class representing edge objects.
    :param graph: (:class:`Graph`) Copy constructor. Copies the input graph into new Kripke object.
    :param file: (str) Name of file (with absolute path) from which to load the Kripke graph.

    .. note:: Kripke structure class is defined as a placeholder. It may be used to define structures similar to
              :class:`TSys`. However, presently not much thought has been given to it.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, alphabet=None, vtype=None, etype=None, graph=None, file=None):

        # Validate input data-types
        assert isinstance(alphabet, Alphabet) or alphabet is None, \
            f"Parameter alphabet must be an Alphabet object. Received type(alphabet)={type(alphabet)}."

        # Base class constructor
        super(Kripke, self).__init__(vtype=vtype, etype=etype, graph=graph, file=file)

        # Defining parameters
        self._alphabet = alphabet                                            # Set of atomic propositions
        self._init_st = None                                                 # Set of initial states

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_left_total(self):
        raise NotImplementedError(f"{self}.is_left_total property is not yet implemented.")       # pragma: no cover

    @property
    def alphabet(self):
        """ Returns the alphabet associated with the Kripke structure. """
        return self._alphabet

    @property
    def init_state(self):
        """ Returns the initial state of the initial state(s) of the Kripke structure as a ``set``. """
        return self._init_st

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def initialize(self, init_st):
        """
        Defines the initial states of the Kripke structure.

        :param init_st: (:class:`Kripke.Vertex` or set of :class:`Kripke.Vertex` objects) Initial state(s) of the
            Kripke structure.
        """
        if isinstance(init_st, Iterable):
            assert all(isinstance(st, Kripke.Vertex) for st in init_st)
            self._init_st = set(init_st)

        else:
            assert isinstance(init_st, Kripke.Vertex)
            assert init_st in self.vertices

            if self._init_st is not None:
                raise AssertionError(f"{self.__class__.__name__} is already initialized. "
                                     f"Reinitialization is not allowed.")

            self._init_st = {init_st}

