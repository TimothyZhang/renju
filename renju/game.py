from renju.rule import Renju, Color, FinishReason


class Listener:
    # todo: player info
    def on_started(self):
        raise NotImplementedError()

    def on_move_made(self, color: Color, row: int, col: int):
        raise NotImplementedError()

    def on_finished(self, winner: Color, reason: FinishReason):
        raise NotImplementedError()


class Game(Renju):
    def __init__(self):
        super().__init__()
        self._listeners = []

    def add_listener(self, listener: Listener):
        assert listener not in self._listeners
        self._listeners.append(listener)

    def remove_listener(self, listener: Listener):
        self._listeners.remove(listener)

    def start(self):
        super().start()

        for l in self._listeners:
            l.on_started()

    def make_move(self, color, row, col):
        super().make_move(color, row, col)

        for l in self._listeners:
            l.on_move_made(color, row, col)

        if self.is_finished():
            for l in self._listeners:
                l.on_finished(self.get_winner(), FinishReason.FIVE)

    def resign(self, color):
        super().resign(color)

        for l in self._listeners:
            l.on_finished(self.get_winner(), FinishReason.RESIGN)
