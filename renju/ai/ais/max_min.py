import random

from renju.ai.base import AI
from renju.rule import BOARD_ROWS, BOARD_COLS, Color, opponent_of, NONE

MAX_SCORE = 2**31
MIN_SCORE = -MAX_SCORE

# SCORE_TABLE[len][blocks]
SCORE_TABLE = (
    (),
    (10, 5, 1),  # 1 stone
    (1000, 500, 10),  # 2 stones
    (100000, 50000, 100),  # 3 stones
    (10000000, 5000000, 1000),  # 4 stones
)

TOP_LEFT_POSITIONS = [(0, col) for col in range(BOARD_COLS)] + [(row, 0) for row in range(BOARD_ROWS)]
TOP_RIGHT_POSITIONS = [(0, col) for col in range(BOARD_COLS)] + [(row, BOARD_COLS-1) for row in range(BOARD_ROWS)]


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
        board = self.renju.board
        for row, col in self.renju.iter_empty_positions():
            for nr, nc in iter_neighbours(row, col):  # only consider positions nearing existing stones.
                if board[nr][nc] != NONE:
                    yield row, col
                    break

    def evaluate(self, color: Color) -> int:
        board = self.renju.board
        opponent = opponent_of(color)

        score = 0
        # horizontal
        for row in range(BOARD_ROWS):
            col = 0
            while col < BOARD_COLS:
                if board[row][col] == NONE:  # skip empty positions
                    col += 1
                    continue

                color2 = board[row][col]
                head = col
                col += 1
                n = 1
                while col < BOARD_COLS and board[row][col] == color2:
                    n += 1
                    col += 1
                tail = col - 1

                if n >= 5:
                    return MAX_SCORE if color == color2 else -MAX_SCORE

                blocks = 0
                if head == 0 or board[row][head-1] == opponent:
                    blocks += 1
                if tail == BOARD_COLS-1 or board[row][tail+1] == opponent:
                    blocks += 1
                score += SCORE_TABLE[n][blocks] if color == color2 else -SCORE_TABLE[n][blocks]

        # vertical
        for col in range(BOARD_COLS):
            row = 0
            while row < BOARD_ROWS:
                if board[row][col] == NONE:
                    row += 1
                    continue

                color2 = board[row][col]
                head = row
                n = 1
                row += 1
                while row < BOARD_ROWS and board[row][col] == color2:
                    n += 1
                    row += 1
                tail = row - 1

                if n >= 5:
                    return MAX_SCORE if color == color2 else -MAX_SCORE

                blocks = 0
                if head == 0 or board[head-1][col] == opponent:
                    blocks += 1
                if tail == BOARD_ROWS-1 or board[tail+1][col] == opponent:
                    blocks += 1

                score += SCORE_TABLE[n][blocks] if color == color2 else -SCORE_TABLE[n][blocks]

        # main diagonal
        for row, col in TOP_LEFT_POSITIONS:
            while row < BOARD_ROWS and col < BOARD_COLS:
                if board[row][col] == NONE:
                    row += 1
                    col += 1
                    continue

                color2 = board[row][col]
                hr, hc = row, col
                row += 1
                col += 1
                n = 1
                while row < BOARD_ROWS and col < BOARD_COLS and board[row][col] == color2:
                    row += 1
                    col += 1
                    n += 1
                tr, tc = row-1, col-1

                if n >= 5:
                    return MAX_SCORE if color == color2 else -MAX_SCORE

                blocks = 0
                if hr == 0 or hc == 0 or board[hr-1][hc-1] == opponent:
                    blocks += 1
                if tr == BOARD_ROWS-1 or tc == BOARD_COLS-1 or board[hr+1][hc+1] == opponent:
                    blocks += 1
                score += SCORE_TABLE[n][blocks] if color == color2 else -SCORE_TABLE[n][blocks]

        # main anti diagonal
        for row, col in TOP_RIGHT_POSITIONS:
            while row < BOARD_ROWS and col >= 0:
                if board[row][col] == NONE:
                    row += 1
                    col -= 1
                    continue

                color2 = board[row][col]
                hr, hc = row, col
                row += 1
                col -= 1
                n = 1
                while row < BOARD_ROWS and col >= 0 and board[row][col] == color2:
                    row += 1
                    col -= 1
                    n += 1
                tr, tc = row-1, col+1

                if n >= 5:
                    return MAX_SCORE if color == color2 else -MAX_SCORE

                blocks = 0
                if hr == 0 or hc == BOARD_COLS-1 or board[hr-1][hc+1] == opponent:
                    blocks += 1
                if tr == BOARD_ROWS-1 or tc == 0 or board[tr+1][tc-1] == opponent:
                    blocks += 1
                score += SCORE_TABLE[n][blocks] if color == color2 else -SCORE_TABLE[n][blocks]

        return score


def iter_neighbours(row, col, distance=1) -> (int, int):
    for dr in range(-distance, distance+1):
        for dc in range(-distance, distance+1):
            if dr == 0 and dc == 0:
                continue

            nr, nc = row + dr, col + dc
            if 0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLS:
                yield nr, nc
