from typing import Type, Iterator

from renju.game.participant import Participant, Player
from .board import Game


class Server(Game):
    def __init__(self):
        super().__init__()
        self.participants = []

    def iter_all_participants(self) -> Iterator[Participant]:
        return iter(self.participants)

    def iter_participants_of_type(self, type_: Type[Participant]) -> Iterator[Participant]:
        for p in self.participants:
            if isinstance(p, type_):
                yield p

    def iter_player_participants(self) -> Iterator[Player]:
        # noinspection PyTypeChecker
        return self.iter_participants_of_type(Player)

    def start(self):
        super().start()

        for p in self.iter_all_participants():
            p.on_started()

    def make_move(self, color, row, col):
        super().make_move(color, row, col)

        for p in self.iter_all_participants():
            p.on_move_made(color, row, col)

        if self.is_finished():
            for p in self.iter_all_participants():
                p.on_finished(self.get_winner())

    def unmake_move(self):
        raise NotImplementedError()

    def resign(self, color):
        super().resign(color)

        for p in self.iter_all_participants():
            p.on_resigned(color)

        for p in self.iter_all_participants():
            p.on_finished(self.get_winner())
