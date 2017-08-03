from renju.rule import Renju, Color, FinishReason


class Listener:
    # todo: player info
    def on_started(self):
        raise NotImplementedError()

    def on_move_made(self, color: Color, row: int, col: int):
        raise NotImplementedError()

    def on_finished(self, winner: Color, reason: FinishReason):
        raise NotImplementedError()


class Game:
    def __init__(self):
        super().__init__()

        self._renju = Renju()
        self._listeners = []

    @property
    def renju(self):
        return self._renju

    def add_listener(self, listener: Listener):
        assert listener not in self._listeners
        self._listeners.append(listener)

    def remove_listener(self, listener: Listener):
        self._listeners.remove(listener)

    def start(self):
        self._renju.start()

        for l in self._listeners:
            l.on_started()

    def make_move(self, color, row, col):
        assert color == self._renju.next_move_color
        self._renju.make_move(row, col)

        for l in self._listeners:
            l.on_move_made(color, row, col)

        if self._renju.is_finished():
            for l in self._listeners:
                l.on_finished(self._renju.get_winner(), FinishReason.FIVE)

    def resign(self, color):
        self._renju.resign(color)

        for l in self._listeners:
            l.on_finished(self._renju.get_winner(), FinishReason.RESIGN)
