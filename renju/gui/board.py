import string
from tkinter import Canvas, RIGHT

from renju.game import Game
from renju.rule import RENJU_SIZE, BLACK
from renju.gui import main_frame

MARGIN = 30
TEXT_SPACING = 8
GRID_SIZE = 30
LINE_WIDTH = 1

LINE_LENGTH = (RENJU_SIZE - 1) * GRID_SIZE + LINE_WIDTH
BOARD_SIZE = LINE_LENGTH + MARGIN * 2

DOT_RADIUS = 3
STONE_RADIUS = 10
STONE_CLICK_RADIUS = 15
# fixme: I have to put a offset, otherwise the board is not in the center of canvas.
CANVAS_OFFSET = 3


class Board(Canvas):
    def __init__(self, frame: 'main_frame.MainFrame'):
        super().__init__(frame, width=BOARD_SIZE, height=BOARD_SIZE, bg='#ddaa22', bd=0)
        self.frame = frame

        # {(row, col): handle}
        self._stones = {}
        """:type: dict[(int, int),int]"""

        self._draw_board()
        self.bind('<Button-1>', self._on_button1_clicked)

    @property
    def game(self) -> Game:
        return self.frame.game

    def _draw_board(self):
        top = left = MARGIN + CANVAS_OFFSET
        bottom, right = top + LINE_LENGTH, left + LINE_LENGTH

        # horizontal lines
        y = top
        for row in range(RENJU_SIZE):
            self.create_line(left, y, right, y)  # Line
            self.create_text(left-TEXT_SPACING, y, justify=RIGHT, text=str(15-row))  # Label
            y += GRID_SIZE

        # vertical lines
        x = left
        for col in range(RENJU_SIZE):
            self.create_line(x, top, x, bottom)  # Line
            self.create_text(x, bottom + TEXT_SPACING, text=string.ascii_uppercase[col])  # Label
            x += GRID_SIZE

        # dots
        dot_rcs = (
            (RENJU_SIZE // 2, RENJU_SIZE // 2),  # center
            (3, 3),
            (3, RENJU_SIZE - 4),
            (RENJU_SIZE - 4, 3),
            (RENJU_SIZE - 4, RENJU_SIZE - 4)
        )
        for row, col in dot_rcs:
            self._draw_circle(self.rc2xy(row, col), DOT_RADIUS, 'black')

    def _draw_circle(self, center: (float, float), radius, color: str):
        x, y = center
        return self.create_oval((x - radius, y - radius, x + radius, y + radius), fill=color)

    def _on_button1_clicked(self, event):
        self._place_stone(event.x, event.y)

    def _place_stone(self, x, y):
        color = self.frame.game.renju.next_move_color
        row, col = self.xy2rc(x, y)
        if row == -1 or col == -1:
            return

        if not self.game.renju.is_playing() or self.game.renju.next_move_color != color:
            return

        if not self.frame.is_human(color):
            return

        if (row, col) in self._stones:
            return

        self.game.make_move(color, row, col)

    def rc2xy(self, row: int, col: int) -> (int, int):
        row, col = row-1, col-1  # row, col starts from 1
        return CANVAS_OFFSET + MARGIN + col * GRID_SIZE, CANVAS_OFFSET + MARGIN + row * GRID_SIZE

    def xy2rc(self, x: float, y: float) -> (int, int):
        col = int(round((x - CANVAS_OFFSET - MARGIN) / GRID_SIZE)) + 1
        row = int(round((y - CANVAS_OFFSET - MARGIN) / GRID_SIZE)) + 1
        x2, y2 = self.rc2xy(row, col)
        if abs(x2-x) > STONE_CLICK_RADIUS or abs(y2-y) > STONE_CLICK_RADIUS:
            return -1, -1
        return row, col

    def add_stone(self, color, row, col):
        assert (row, col) not in self._stones
        self._stones[(row, col)] = self._draw_circle(self.rc2xy(row, col),
                                                     STONE_RADIUS,
                                                     'black' if color == BLACK else 'white')

    def remove_stone(self, row, col):
        stone = self._stones.pop((row, col))
        self.delete(stone)

    def reset(self):
        for stone in self._stones.values():
            self.delete(stone)
        self._stones.clear()

        # # bg
        # image = Image.open("images/board.jpg")
        # image = image.resize((512, 512), resample=Image.BICUBIC)
        # self.bg_image = photo_image = ImageTk.PhotoImage(image)
        # self..create_image((0, 0), anchor=NW, image=photo_image)

        # line = self..create_line(0, 0, 200, 100)
        # self..itemconfig(line, tags=('haha', 'hehe'))
        # self..addtag_withtag("blabla", "haha")
        # self..gettags(line)
        # self..find_withtag('haha')

    # def on_stone_clicked(self, event):
    #     canvas = event.widget
    #     x = canvas.canvasx(event.x)
    #     y = canvas.canvasy(event.y)
    #     canvas.find_closest(x, y)

