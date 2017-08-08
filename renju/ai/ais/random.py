import random

from renju.ai.base import AI
from renju.rule import Renju, BOARD_SIZE, NONE


class RenjuWrapper(Renju):
    """
    Expose some protected members for AI
    """
    @property
    def board(self):
        return self._board

    def iter_empty_positions(self):
        board = self.board
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == NONE:
                    yield row, col


class RandomAI(AI):
    renju_class = RenjuWrapper

    def get_move(self) -> (int, int):
        return random.choice(list(self.renju.iter_empty_positions()))
