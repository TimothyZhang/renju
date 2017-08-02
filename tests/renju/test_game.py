from unittest import TestCase

from renju.rule.renju import Renju


class TestRenju(Renju):
    @property
    def board(self):
        return self._board

    def replay(self, history):
        assert not self._history
        self._history = history


class GameTest(TestCase):
    def setUp(self):
        self.game = TestRenju()

    def test_win(self):
        self.game.start()
        # self.game.replay(((0, 0), (0, 1)))
        # todo ..
