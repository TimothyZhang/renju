from tkinter import Frame, LEFT, Button, RIGHT, GROOVE

from renju.game import Listener, Game
from renju.gui.board import Board
from renju.rule import Color


class MainFrame(Frame, Listener):
    def __init__(self, app):
        super().__init__(app)

        self.game = Game()
        self.game.add_listener(self)

        self._init_gui()

    def _init_gui(self):
        self.board = Board(self)
        self.board.pack(side=LEFT)

        btn = Button(self, name='test', text='TEST', fg='red', relief=GROOVE)
        btn.config(command=btn.flash)
        btn.pack(side=RIGHT)
        btn.flash()

    def on_move_unmade(self):
        pass

    def on_finished(self, winner: Color):
        pass

    def on_resigned(self, color: Color):
        pass

    def on_move_made(self, color: Color, row: int, col: int):
        self.board.add_stone(color, row, col)

    def on_started(self):
        pass
