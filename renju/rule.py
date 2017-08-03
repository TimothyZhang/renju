from enum import Enum
from typing import NewType

Color = NewType('Color', int)

NONE = Color(0)
BLACK = Color(1)
WHITE = Color(2)

# board size
BOARD_COLS = 15
BOARD_ROWS = 15

# todo need a better name
FIVE = 5


def get_color_name(color: Color):
    if color == NONE:
        return 'none'
    if color == BLACK:
        return 'black'
    if color == WHITE:
        return 'white'


def opponent_of(color: Color) -> Color:
    assert color != NONE
    return WHITE if color == BLACK else BLACK


class FinishReason(Enum):
    FIVE = 0
    FORBIDDEN = 1
    RESIGN = 2


class Renju:
    def __init__(self):
        self._board = [[NONE] * BOARD_ROWS for _ in range(BOARD_COLS)]
        """:type: List[List[Color]]"""

        # todo is there an official name?
        self._history = []
        self._winner = NONE
        self._finish_reason = FIVE
        self._started = False

    def start(self):
        self._board = [[NONE] * BOARD_ROWS for _ in range(BOARD_COLS)]
        self._history = []
        self._winner = NONE
        self._finish_reason = FIVE
        self._started = True

    def make_move(self, color: Color, row: int, col: int):
        assert self._board[row][col] == NONE
        assert self.next_move_color == color

        self._board[row][col] = color
        self._history.append((row, col))
        self._check_finished()

    def resign(self, color: Color):
        self._winner = opponent_of(color)
        self._finish_reason = FinishReason.RESIGN

    @property
    def next_move_color(self) -> Color:
        last = self.last_moved_color
        return BLACK if last == NONE else opponent_of(last)

    @property
    def last_moved_color(self) -> Color:
        if not self._history:
            return NONE

        return BLACK if len(self._history) % 2 == 1 else WHITE

    def get_winner(self) -> Color:
        return self._winner

    def is_started(self) -> bool:
        return self._started

    def is_finished(self) -> bool:
        return self._winner != NONE

    def is_playing(self) -> bool:
        return self.is_started() and not self.is_finished()

    def _finish(self, color: Color, reason: FinishReason):
        self._winner = color
        self._finish_reason = reason

    def _check_finished(self):
        """        
        Checks whether the last move ends the game. 
        """
        # todo support Renju rules.
        if self.is_finished():
            return

        if not self._history:
            return

        board = self._board
        row, col = self._history[-1]
        color = board[row][col]

        # horizontal
        n = 1
        for c in range(col-1, max(col-FIVE, 0), -1):
            if board[row][c] != color:
                break
            n += 1
        for c in range(col+1, min(col+FIVE, BOARD_COLS)):
            if board[row][c] != color:
                break
            n += 1

        if n >= FIVE:
            self._finished = True
            self._winner = self.last_moved_color
            return

        # vertical
        n = 1
        for r in range(row-1, max(row-FIVE, 0), -1):
            if board[r][col] != color:
                break
            n += 1
        for r in range(row+1, min(row+FIVE, BOARD_ROWS)):
            if board[r][col] != color:
                break
        if n >= FIVE:
            return True

        # main diagonal
        n = 1
        r, c = row-1, col-1
        while r >= 0 and c >= 0 and board[r][c] == color:
            n += 1
            r -= 1
            c -= 1

        r, c = row+1, col+1
        while r < BOARD_ROWS and c < BOARD_COLS and board[r][c] == color:
            n += 1
            r += 1
            c += 1

        if n >= FIVE:
            return True

        # anti diagonal
        n = 1
        r, c = row-1, col+1
        while r >= 0 and c < BOARD_COLS and board[r][c] == color:
            n += 1
            r -= 1
            c += 1

        r, c = row+1, col-1
        while r < BOARD_ROWS and c >= 0 and board[r][c] == color:
            n += 1
            r += 1
            c -= 1

        if n >= FIVE:
            return True

        return False

#
# def iterate_rows():
#     def row_iterator(row_):
#         for col in range(BOARD_SIZE):
#             yield row_, col
#
#     for row in range(BOARD_SIZE):
#         yield row_iterator(row)
#
#
# def iterate_cols():
#     def col_iterator(col_):
#         for row in range(BOARD_SIZE):
#             yield row, col_
#
#     for col in range(BOARD_SIZE):
#         yield col_iterator(col)
#
#
# # todo how to name the two diagonals?
# def iterate_main_diagonal():
#
#
# def iterate_lines():
#     return itertools.chain(iterate_rows(), iterate_cols())
#
#
# if __name__ == '__main__':
#     for line in iterate_lines():
#         for r, c in line:
#             print(r, c)
