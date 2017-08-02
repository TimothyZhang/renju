from renju.rule.const import Color, NONE
from renju.game import Server


class Participant:
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


# noinspection PyAbstractClass
class Player(Participant):
    """A player can make a move, unmake a move(only if allowed), or resign"""
    color = NONE

    def __init__(self, server: Server):
        self.server = server

    def make_move(self, row, col):
        self.server.make_move(self.color, row, col)

    def unmake_move(self):
        raise NotImplementedError()

    def resign(self):
        self.server.resign(self.color)


# noinspection PyAbstractClass
class Judge(Participant):
    """The judge determines when the game starts."""
    def start(self):
        raise NotImplementedError()


# noinspection PyAbstractClass
class Spectator(Participant):
    """A spectator can do nothing ."""
    pass
