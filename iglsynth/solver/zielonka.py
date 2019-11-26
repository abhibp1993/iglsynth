"""
Implementation of Zielonka Solver.
"""

from iglsynth.util.graph import *
from iglsynth.solver.core import *


class ZielonkaSolver(ISolver):
    def __init__(self, game):
        super(ZielonkaSolver, self).__init__(game)

        self._p1_win = set()
        self._p2_win = set()
        self._p1_strategy = Graph(vtype=game.vtype, etype=game.etype)
        self._p2_strategy = Graph(vtype=game.vtype, etype=game.etype)

    @property
    def p1_win(self):
        return self._p1_win

    @property
    def p2_win(self):
        return self._p2_win

    @property
    def p1_strategy(self):
        return self._p1_strategy

    @property
    def p2_strategy(self):
        return self._p2_strategy

    def _validate_game(self):
        assert type(self._game) == Game
        assert self._game.kind == TURN_BASED

    def _pre1(self):

        # Initialize an empty set
        pre1 = set()

        # Iterate over all states in winning region
        for v in self._p1_win:

            # Iterate over all incoming edges to check all potential states to add to Pre1
            for e in self._game.in_edges(v):

                # Get the candidate vertex to add to Pre1
                u = e.source

                # If u is P1's vertex and not already added, then add it to Pre1
                if u.turn == 1 and u not in self._p1_win:
                    pre1.add(u)

        return pre1

    def _pre2(self):
        # Initialize an empty set
        pre2 = set()

        # Iterate over all states in winning region
        for v in self._p1_win:

            # Iterate over all incoming edges to check all potential states to add to Pre1
            for e in self._game.in_edges(v):

                # Get the candidate vertex to add to Pre1
                u = e.source

                # If u is P2's vertex AND not already added AND all outgoing edges are winning, then add it to Pre1
                if u.turn == 2 and u not in self._p1_win and set(self._game.out_neighbors(u)).issubset(self._p1_win):
                    pre2.add(u)

        return pre2

    def _losing_strategy(self):
        pass

    def configure(self):
        pass

    def solve(self):

        # Initialize/Reset Solution data structures
        final = set()
        for v in self._game.vertices:
            self._p1_strategy.add_vertex(v)
            self._p2_strategy.add_vertex(v)
            if v in self._game.final:
                final.add(v)

        # Zielonka's algorithm
        self._p1_win = final
        while True:
            pre1 = self._pre1()
            pre2 = self._pre2()
            p1_win = set.union(self._p1_win, pre1, pre2)

            if p1_win == self._p1_win:
                break

            self._p1_win = p1_win

        # Update winning region for P2
        self._p2_win = set.difference(set(self._game.vertices), self._p1_win)

        # Update P1 and P2 strategy at their respective losing states
        self._losing_strategy()
