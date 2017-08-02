from renju.rule import Renju, Color


class Server(Renju):
    def __init__(self):
        super().__init__()
        self._listeners = []

    def add_listener(self, listener: Listener):
        self._listeners.append(listener)

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
                l.on_finished(self.get_winner())

    def unmake_move(self):
        raise NotImplementedError()

    def resign(self, color):
        super().resign(color)

        for l in self._listeners:
            l.on_resigned(color)

        for l in self._listeners:
            l.on_finished(self.get_winner())


class Listener:
    # todo: player info
    def on_started(self):
        raise NotImplementedError()

    def on_move_made(self, color: Color, row: int, col: int):
        raise NotImplementedError()

    def on_move_unmade(self):
        raise NotImplementedError()

    def on_resigned(self, color: Color):
        raise NotImplementedError()

    def on_finished(self, winner: Color):
        raise NotImplementedError()
