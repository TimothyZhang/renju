from enum import Enum
from tkinter import Frame, LEFT, Button, RIGHT, messagebox, DISABLED, NORMAL, TOP

from renju.ai.ais.alpha_beta import AlphaBetaAI
from renju.ai.ais.max_min import MaxMinAI
from renju.ai.ais.random import RandomAI
from renju.ai.base import AIHelper
from renju.game import Listener, Game
from renju.gui.board import Board
from renju.rule import Color, get_color_name, FinishReason, WHITE, NONE, opponent_of, BLACK


class GameMode(Enum):
    ONE_PLAYER = 1
    TWO_PLAYERS = 2


class MainFrame(Frame, Listener):
    def __init__(self, app):
        super().__init__(app)

        self.game = Game()
        self.game.add_listener(self)

        self._init_gui()
        self.game_mode = GameMode.ONE_PLAYER

        self.ai_color = NONE
        self.ai_helper = None
        """:type: AIHelper"""

    @property
    def human_color(self):
        return opponent_of(self.ai_color)

    def is_human(self, color: Color):
        if self.game_mode == GameMode.TWO_PLAYERS:
            return True

        return color == self.human_color

    def _init_gui(self):
        self.board = Board(self)
        self.board.pack(side=LEFT)

        self.start_1p_button = Button(self, name='1p', text='1P', fg='blue', command=self._start_one_player)
        self.start_1p_button.pack(side=TOP)

        self.start_2p_button = Button(self, name='2p', text='2P', fg='blue', command=self._start_two_player)
        self.start_2p_button.pack(side=TOP)

        self.regret_button = Button(self, name='regret', text='Regret', fg='red', command=self._regret, state=DISABLED)
        self.regret_button.pack(side=TOP)

    def _start_one_player(self):
        self.game.start()
        self.game_mode = GameMode.ONE_PLAYER
        self.ai_color = WHITE

        self.ai_helper = AIHelper(self.game)
        self.ai_helper.reset(AlphaBetaAI, WHITE)

        self.game.start()
        self._set_start_button_stats(DISABLED)

    def _start_two_player(self):
        self.game_mode = GameMode.TWO_PLAYERS
        self.game.start()
        self._set_start_button_stats(DISABLED)

    def _set_start_button_stats(self, state):
        self.start_1p_button.config(state=state)
        self.start_2p_button.config(state=state)

    def _regret(self):
        self.game.regret()

    def on_finished(self, winner: Color, reason: FinishReason):
        self._set_start_button_stats(NORMAL)

        self.regret_button.config(state=DISABLED)
        messagebox.showinfo('Finished', 'Winner: %s\nReason: %s' % (get_color_name(winner), reason))

    def on_move_made(self, color: Color, row: int, col: int):
        self.board.add_stone(color, row, col)

        if self.game.renju.next_move_color == self.ai_color:
            self.after(1, self.ai_move)

    def on_move_unmade(self, row, col):
        self.board.remove_stone(row, col)

    def on_started(self):
        self.board.reset()

        self.regret_button.config(state=NORMAL)

        if self.game.renju.next_move_color == self.ai_color:
            self.after(1, self.ai_move)

    def ai_move(self):
        self.ai_helper.move()
