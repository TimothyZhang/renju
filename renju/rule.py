import string
from enum import Enum
from typing import NewType

Color = NewType('Color', int)

NONE = Color(0)
BLACK = Color(1)
WHITE = Color(2)
WALL = Color(3)

RENJU_SIZE = 15
BOARD_SIZE = RENJU_SIZE + 2

# todo need a better name
FIVE = 5


def get_color_name(color: Color):
    if color == NONE:
        return 'none'
    if color == BLACK:
        return 'black'
    if color == WHITE:
        return 'white'


# todo rename all position to slot
def get_position_name(row, col):
    return string.ascii_uppercase[col] + str(row+1)


def opponent_of(color: Color) -> Color:
    assert color != NONE
    return WHITE if color == BLACK else BLACK


class FinishReason(Enum):
    FIVE = 0
    FORBIDDEN = 1
    RESIGN = 2


class RenjuState(Enum):
    PREPARE = 0
    COMPETING = 1
    FINISHED = 2


# todo support Renju rules.
class Renju:
    """
    Holds core rule of Renju, used by both Game and AI.
    """

    def __init__(self):
        self._board = []
        """:type: List[List[Color]]"""

        # todo is there an official name? ply?
        self._history = []
        self._state = RenjuState.PREPARE
        self._winner = NONE
        self._finish_reason = FIVE

    def start(self):
        self._board = [[WALL] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self._history = []
        self._state = RenjuState.COMPETING
        self._winner = NONE
        self._finish_reason = FIVE

    def make_move(self, row: int, col: int):
        self._board[row][col] = self.next_move_color
        self._history.append((row, col))
        self._check_finished()

    def unmake_move(self):
        row, col = self._history.pop()
        self._board[row][col] = NONE

        # self._winner = NONE
        # self._state = RenjuState.COMPETING
        return row, col

    def resign(self):
        self._finish(opponent_of(self.next_move_color),  FinishReason.RESIGN)

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

    def is_playing(self) -> bool:
        return self._state == RenjuState.COMPETING

    def has_finished(self) -> bool:
        return self._state == RenjuState.FINISHED

    def _finish(self, color: Color, reason: FinishReason):
        self._winner = color
        self._finish_reason = reason
        self._state = RenjuState.FINISHED

    def _check_finished(self):
        """        
        Checks whether the last move ends the game. 
        """
        if self.has_finished():
            return

        if not self._history:
            return

        board = self._board
        row, col = self._history[-1]
        color = board[row][col]

        # horizontal
        n = 1
        c = col - 1
        while board[row][c] == color:
            n += 1
            c -= 1
        c = col + 1
        while board[row][c] == color:
            n += 1
            c += 1

        if n >= FIVE:
            return self._finish(color, FinishReason.FIVE)

        # vertical
        n = 1
        r = row - 1
        while board[r][col] == color:
            n += 1
            r -= 1
        r = row + 1
        while board[r][col] == color:
            n += 1
            r += 1

        if n >= FIVE:
            return self._finish(color, FinishReason.FIVE)

        # main diagonal
        n = 1
        r, c = row-1, col-1
        while board[r][c] == color:
            n += 1
            r -= 1
            c -= 1
        r, c = row+1, col+1
        while board[r][c] == color:
            n += 1
            r += 1
            c += 1

        if n >= FIVE:
            return self._finish(color, FinishReason.FIVE)

        # anti diagonal
        n = 1
        r, c = row-1, col+1
        while board[r][c] == color:
            n += 1
            r -= 1
            c += 1

        r, c = row+1, col-1
        while board[r][c] == color:
            n += 1
            r += 1
            c -= 1

        if n >= FIVE:
            return self._finish(color, FinishReason.FIVE)
