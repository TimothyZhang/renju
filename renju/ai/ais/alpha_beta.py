from renju.ai.ais.max_min import MaxMinAI, MAX_SCORE
from renju.ai.base import AI
from renju.rule import Renju, BOARD_SIZE, NONE


"""
ooooo: 1
"""
class RenjuWrapper(Renju):
    """
    Expose some protected members for AI
    """
    @property
    def board(self):
        return self._board

    def iter_empty_positions(self):
        board = self.board
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == NONE:
                    yield row, col

    def evaluate(self) -> int:
        pass


class AlphaBetaAI(AI):
    renju_class = RenjuWrapper
    evaluated = 0
    pruned = 0

    def get_move(self) -> (int, int):
        self.evaluated = self.pruned = 0
        _, move = self.alpha_beta(4, -MAX_SCORE, MAX_SCORE)
        print('searched: %s, prunded: %s, pruned %%: %.2f%%' % (self.evaluated, self.pruned,
                                                                self.pruned * 100 / (self.evaluated + self.pruned)))
        return move

    def alpha_beta(self, depth: int, alpha: int, beta: int) -> (int, (int, int)):
        if depth == 0:
            self.evaluated += 1
            return self.evaluate(self.renju.next_move_color), None
        if self.renju.is_finished():
            return -MAX_SCORE, None

        moves = self.generate_moves()
        if depth >= 3:
            print('  ' * (4-depth), 'moves: %s' % len(moves))
        max_move = None
        for i, (row, col) in enumerate(moves):
            if depth >= 3:
                print('  ' * (4-depth), '  move %s: %s, %s' % (i, row, col))
            self.renju.make_move(row, col)

            score, move = self.alpha_beta(depth-1, -beta, -alpha)
            score = -score

            if score > beta:
                self.pruned += (2 ** depth - 1) * (len(moves) - i - 1)
                self.renju.unmake_move()
                return MAX_SCORE, None

            if score > alpha:
                alpha = score
                max_move = row, col
            self.renju.unmake_move()

        return alpha, max_move

    # def generate_moves(self):
    #     board = self.renju.board
    #     moves = []
    #     color = self.renju.next_move_color
    #
    #     for row, col in self.renju.iter_empty_positions():
    #         for nr, nc in iter_neighbours(row, col):  # only consider positions nearing existing stones.
    #             if board[nr][nc] != NONE:
    #                 moves.append((row, col))
    #     return moves
