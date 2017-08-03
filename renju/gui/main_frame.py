from tkinter import Frame, LEFT, Button, RIGHT, GROOVE, messagebox, DISABLED, NORMAL

from renju.game import Listener, Game
from renju.gui.board import Board
from renju.rule import Color, get_color_name, FinishReason


class MainFrame(Frame, Listener):
    def __init__(self, app):
        super().__init__(app)

        self.game = Game()
        self.game.add_listener(self)

        self._init_gui()

    def _init_gui(self):
        self.board = Board(self)
        self.board.pack(side=LEFT)

        self.start_button = Button(self, name='start', text='Start', fg='red', relief=GROOVE, command=self._start)
        # btn.config(command=btn.flash)
        self.start_button.pack(side=RIGHT)
        self.start_button.flash()

    def _start(self):
        self.game.start()
        self.start_button.config(state=DISABLED)

    def on_move_unmade(self):
        pass

    def on_finished(self, winner: Color, reason: FinishReason):
        messagebox.showinfo('Finished', 'Winner: %s\nReason: %s' % (get_color_name(winner), reason))
        self.start_button.config(state=NORMAL)

    def on_move_made(self, color: Color, row: int, col: int):
        self.board.add_stone(color, row, col)

    def on_started(self):
        self.board.reset()
