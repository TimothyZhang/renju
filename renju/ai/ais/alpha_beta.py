from renju.ai.ais.max_min import MaxMinAI, MAX_SCORE


class AlphaBetaAI(MaxMinAI):
    evaluated = 0
    pruned = 0

    def get_move(self) -> (int, int):
        self.evaluated = self.pruned = 0
        _, move = self.alpha_beta(4, -MAX_SCORE, MAX_SCORE)
        print('pruned: %.2f%%' % (self.pruned * 100 / (self.evaluated + self.pruned)))
        return move

    def alpha_beta(self, depth: int, alpha: int, beta: int) -> (int, (int, int)):
        if depth == 0:
            self.evaluated += 1
            return self.evaluate(self.renju.next_move_color), None
        if self.renju.is_finished():
            return -MAX_SCORE, None

        max_move = None
        for row, col in self.iter_moves():
            self.renju.make_move(row, col)

            score, move = self.alpha_beta(depth-1, -beta, -alpha)
            score = -score

            if score > beta:
                self.pruned += 1
                self.renju.unmake_move()
                return MAX_SCORE, None

            if score > alpha:
                alpha = score
                max_move = row, col
            self.renju.unmake_move()

        return alpha, max_move
