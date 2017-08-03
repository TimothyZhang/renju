from renju.game import Listener, Game
from renju.rule import Renju, Color, FinishReason, NONE, BLACK


class AI:
    def get_move(self, renju: 'RenjuForAI') -> (int, int):
        raise NotImplementedError()


class RenjuForAI(Renju):
    @property
    def board(self):
        return self._board


class AIHelper(Listener):
    def __init__(self, game: Game, ai: AI):
        self.game = game
        self.game.add_listener(self)

        self.renju = RenjuForAI()
        self.ai = ai
        self.color = NONE

    def set_color(self, color: Color):
        self.color = color

    def on_finished(self, winner: Color, reason: FinishReason):
        pass

    def on_started(self):
        self.renju.start()

        if self.color == BLACK:
            self._move()

    def on_move_made(self, color: Color, row: int, col: int):
        self.renju.make_move(color, row, col)

        if color != self.color:
            self._move()

    def _move(self):
        row, col = self.ai.get_move(self.renju)
        self.game.make_move(self.color, row, col)
