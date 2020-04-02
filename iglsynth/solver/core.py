from iglsynth.model.game import *


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


class Strategy(SubGraph):
    # TODO: Update this after defining SubGraph class
    pass
