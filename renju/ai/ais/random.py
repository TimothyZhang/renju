import random

from renju.ai.base import AI


class RandomAI(AI):
    def get_move(self) -> (int, int):
        return random.choice(list(self.renju.iter_empty_positions()))
