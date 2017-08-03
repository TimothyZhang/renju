import random

from renju.ai.base import AI
from renju.rule import BOARD_ROWS, BOARD_COLS, Color, opponent_of

MAX_SCORE = 2**31
MIN_SCORE = -MAX_SCORE


class MaxMinAI(AI):
    def get_move(self) -> (int, int):
        _, move = self.max_min(2)
        return move

    def max_min(self, depth: int) -> (int, (int, int)):
        if depth == 0:
            return self.evaluate(self.renju.next_move_color), None

        max_score, max_move = MIN_SCORE, None
        for row, col in self.iter_moves():
            self.renju.make_move(row, col)

            if self.renju.is_finished():  # game over
                if self.renju.get_winner() == self.renju.last_moved_color:
                    score = MAX_SCORE
                else:
                    score = -1
            else:
                score, _ = self.max_min(depth-1)
                score = -score

            if score > max_score:
                max_score = score
                max_move = row, col
            self.renju.unmake_move()

        return max_score, max_move

    def iter_moves(self):
        return self.renju.iter_empty_positions()

    def evaluate(self, color: Color) -> int:
        board = self.renju.board
        opponent = opponent_of(color)

        score = 0
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] != color:
                    continue

                for nr, nc in iter_neighbours(row, col):
                    if board[nr][nc] == color:
                        score += 1
                    elif board[nr][nc] == opponent:
                        score += 2
                    else:
                        score += 0
        return score


def iter_neighbours(row, col) -> (int, int):
    for dr, dc in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        nr, nc = row + dr, col + dc
        if 0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLS:
            yield nr, nc
