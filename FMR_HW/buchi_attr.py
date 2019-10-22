"""
HW Problem 3 for Formal Methods in Robotics.
    Implement the `BuchiSolver` for constructing identifying
    a winning region for the robot and its environment.

Instructor: Jie Fu
Author: Abhishek N. Kulkarni
"""


class BuchiGameSolver:
    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, game):
        assert self._validate_game(game)

        self._game = game
        self._attr = None
        self._strategy = None

    # ------------------------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def _validate_game(self, game):
        pass

    def _recur(self, final):
        pass

    def _0_attr(self, final):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        final = self._game.final
        # TODO: Your algorithm


