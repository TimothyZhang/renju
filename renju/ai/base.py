from typing import Type

from renju.game import Listener, Game
from renju.rule import Renju, Color, FinishReason, NONE, BLACK, BOARD_SIZE, get_position_name, get_color_name


class AI:
    renju_class = Renju

    def __init__(self, color: Color):
        self.color = color
        self.renju = self.renju_class()

    def get_move(self) -> (int, int):
        raise NotImplementedError()


class AIHelper(Listener):
    def __init__(self, game: Game):
        self.game = game
        self.game.add_listener(self)

        self.ai = None
        """:type: AI"""
        self.color = NONE

    def reset(self, ai: AI, color: Color):
        self.ai = ai
        self.color = color

    @property
    def renju(self):
        return self.ai.renju

    def on_finished(self, winner: Color, reason: FinishReason):
        self.game.remove_listener(self)

    def on_started(self):
        self.renju.start()

    def on_move_made(self, color: Color, row: int, col: int):
        # sync board state
        self.renju.make_move(row, col)
        print('%s: %s' % (get_color_name(color), get_position_name(row, col)))

    def on_move_unmade(self, row, col):
        self.renju.unmake_move()

    def move(self):
        move = self.ai.get_move()
        if move is None:
            self.game.resign()
        else:
            row, col = move
            self.game.make_move(self.color, row, col)
