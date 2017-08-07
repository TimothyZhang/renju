from renju.ai.base import AI
from renju.rule import BOARD_ROWS, BOARD_COLS, Color, opponent_of, NONE

MAX_SCORE = 2**31

TOP_LEFT_POSITIONS = [(0, col) for col in range(BOARD_COLS)] + [(row, 0) for row in range(1, BOARD_ROWS)]
TOP_RIGHT_POSITIONS = [(0, col) for col in range(BOARD_COLS)] + [(row, BOARD_COLS-1) for row in range(1, BOARD_ROWS)]


# Lines
LINES = []
""":type: list[list[(int, int)]]"""

WALL = Color(3)

# SCORE_TABLE[len][blocks]
SINGLE_SEGMENT_SCORES = (
    (),
    (1, 5, 10),  # xox, xo-, -o-
    (10, 100, 1000),  # xoox, xoo-, -oo-
    (100, 1000, 10000),  # xooox, xooo-, -ooo-
    (1000, 9000, 1000000),  # xoooox, xoooo-, -oooo-
)

MULTI_SEGMENT_SCORES = (
    (),
    (),
    (50, 500, 1000),  # xo-ox, xo-o-, -o-o-
    (500, 4500, 10000),  # xo-oox, xo-oo-, -o-oo-
    (9000, 10000, 10000),  # xo-ooox/xoo-oox, xo-ooo-/xoo-oo-, -o-ooo-/-oo-oo-
)


def init_lines():
    if LINES:
        return

    # horizontal
    for row in range(BOARD_ROWS):
        LINES.append([(row, col) for col in range(BOARD_COLS)])

    # vertical
    for col in range(BOARD_COLS):
        LINES.append([(row, col) for row in range(BOARD_ROWS)])

    # main diagonal
    for row, col in TOP_LEFT_POSITIONS:
        line = []
        while row<BOARD_ROWS and col<BOARD_COLS:
            line.append((row, col))
            row += 1
            col += 1
        LINES.append(line)

    # main anti diagonal
    for row, col in TOP_RIGHT_POSITIONS:
        line = []
        while row<BOARD_ROWS and col>=0:
            line.append((row, col))
            row += 1
            col -= 1
        LINES.append(line)
init_lines()


class MaxMinAI(AI):
    def get_move(self) -> (int, int):
        _, move = self.max_min(2)
        return move

    def max_min(self, depth: int) -> (int, (int, int)):
        if depth == 0:
            return self.evaluate(self.renju.next_move_color), None
        if self.renju.is_finished():
            return -MAX_SCORE, None

        max_score, max_move = -MAX_SCORE, None
        for row, col in self.generate_moves():
            self.renju.make_move(row, col)

            score, _ = self.max_min(depth-1)
            score = -score

            if score > max_score:
                max_score = score
                max_move = row, col
            self.renju.unmake_move()

        return max_score, max_move

    def generate_moves(self):
        board = self.renju.board
        moves = []

        for row, col in self.renju.iter_empty_positions():
            for nr, nc in iter_neighbours(row, col, 2):  # only consider positions nearing existing stones.
                if board[nr][nc] != NONE:
                    moves.append((row, col))
        return moves

    def evaluate(self, for_color: Color) -> int:
        board = self.renju.board

        scores = [0, 0, 0]
        for line in LINES:
            segments = [[WALL, 1]]  # [[color, count]...]
            for row, col in line:
                stone = board[row][col]
                if stone == segments[-1][0]:
                    segments[-1][1] += 1
                else:
                    segments.append([stone, 1])
            segments.append([WALL, 1])

            for i in range(1, len(segments)-1):
                color, count = segments[i]
                if color == NONE:  # skip empty positions
                    continue

                if count >= 5:  # five in a row, win!
                    return MAX_SCORE if color == for_color else -MAX_SCORE

                # 2 segments with same color
                if segments[i+1][0] == NONE and segments[i+1][1] == 1 and segments[i+2][0] == color:
                    count2 = segments[i+2][1]
                    total_count = count + count2

                    opens, open_count = 0, 0
                    if segments[i-1][0] == NONE:
                        opens += 1
                        open_count += segments[i-1][1]
                    if segments[i+3][0] == NONE:
                        opens += 1
                        open_count += segments[i+3][1]

                    scores[color] += MULTI_SEGMENT_SCORES[min(4, total_count)][opens]
                    continue

                # single segment
                opens = int(segments[i - 1][0] == NONE) + int(segments[i + 1] == NONE)
                scores[color] += SINGLE_SEGMENT_SCORES[count][opens]
        return scores[for_color] - scores[opponent_of(for_color)]


def iter_neighbours(row, col, distance=1) -> (int, int):
    for dr in range(-distance, distance+1):
        for dc in range(-distance, distance+1):
            if dr == 0 and dc == 0:
                continue

            nr, nc = row + dr, col + dc
            if 0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLS:
                yield nr, nc
