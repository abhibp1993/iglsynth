from iglsynth.game.core import *


class Solver(abc.ABC):
    def __init__(self, game: IGame):
        if self._validate_game(game) is False:
            raise ValueError("Game Validation Failed!! This solver cannot be used for the provided game.")

        self._game = game

    @property
    def game(self):
        return self._game

    @abc.abstractmethod
    def _validate_game(self, game: IGame) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def configure(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

