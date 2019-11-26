from iglsynth.game.game import *


class ISolver(object):
    def __init__(self, game):
        assert isinstance(game, Game)
        self._game = game

    def _validate_game(self):
        pass

    def configure(self):
        pass

    def solve(self):
        pass

