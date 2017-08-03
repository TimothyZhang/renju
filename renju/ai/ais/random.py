import random

from renju.ai.base import AI, RenjuForAI
from renju.rule import NONE, BOARD_ROWS, BOARD_COLS


class RandomAI(AI):
    def get_move(self, renju: RenjuForAI) -> (int, int):
        points = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if renju.board[row][col] == NONE]
        return random.choice(points)
