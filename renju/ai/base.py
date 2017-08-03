from typing import Type

from renju.game import Listener, Game
from renju.rule import Renju, Color, FinishReason, NONE, BLACK, BOARD_COLS, BOARD_ROWS


class AI:
    def __init__(self, renju: 'RenjuWrapper', color: Color):
        self.renju = renju
        self.color = color

    def get_move(self) -> (int, int):
        raise NotImplementedError()


class RenjuWrapper(Renju):
    """
    Expose some protected members for AI
    """
    @property
    def board(self):
        return self._board

    def iter_empty_positions(self):
        board = self.board
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == NONE:
                    yield row, col


class AIHelper(Listener):
    def __init__(self, game: Game):
        self.game = game
        self.game.add_listener(self)

        self.renju = RenjuWrapper()
        self.ai = None
        """:type: AI"""
        self.color = NONE

    def reset(self, ai_class: Type[AI], color: Color):
        self.ai = ai_class(self.renju, color)
        self.color = color

    def on_finished(self, winner: Color, reason: FinishReason):
        self.game.remove_listener(self)

    def on_started(self):
        self.renju.start()

        if self.color == BLACK:
            self._move()

    def on_move_made(self, color: Color, row: int, col: int):
        # sync board state
        self.renju.make_move(row, col)

        # My turn
        if not self.renju.is_finished() and self.renju.next_move_color == self.color:
            self._move()

    def on_move_unmade(self, row, col):
        self.renju.unmake_move()

    def _move(self):
        move = self.ai.get_move()
        if move is None:
            self.game.resign(self.color)
        else:
            row, col = move
            self.game.make_move(self.color, row, col)
