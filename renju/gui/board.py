from tkinter import Canvas

from renju.game import Game
from renju.rule import BOARD_ROWS, BOARD_COLS, BLACK, WHITE, Color
from renju.gui import main_frame

MARGIN = 10
GRID_SIZE = 40
LINE_WIDTH = 1
assert BOARD_COLS == BOARD_ROWS

LINE_LENGTH = (BOARD_COLS - 1) * GRID_SIZE + LINE_WIDTH
BOARD_SIZE = LINE_LENGTH + MARGIN * 2

DOT_RADIUS = 3
STONE_RADIUS = 10
STONE_CLICK_RADIUS = 20
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
        self.bind('<Button-3>', self._on_button3_clicked)

    @property
    def game(self) -> Game:
        return self.frame.game

    def _draw_board(self):
        top = left = MARGIN + CANVAS_OFFSET
        bottom, right = top + LINE_LENGTH, left + LINE_LENGTH

        # horizontal lines
        y = top
        for row in range(BOARD_ROWS):
            self.create_line(left, y, right, y)
            y += GRID_SIZE

        # vertical lines
        x = left
        for col in range(BOARD_COLS):
            self.create_line(x, top, x, bottom)
            x += GRID_SIZE

        # dots
        dot_rcs = (
            (BOARD_ROWS // 2, BOARD_COLS // 2),  # center
            (3, 3),
            (3, BOARD_COLS - 4),
            (BOARD_ROWS - 4, 3),
            (BOARD_ROWS - 4, BOARD_COLS - 4)
        )
        for row, col in dot_rcs:
            self._draw_circle(self.rc2xy(row, col), DOT_RADIUS, 'black')

    def _draw_circle(self, center: (float, float), radius, color: str):
        x, y = center
        return self.create_oval((x - radius, y - radius, x + radius, y + radius), fill=color)

    def _on_button1_clicked(self, event):
        self._place_stone(BLACK, event.x, event.y)

    def _on_button3_clicked(self, event):
        self._place_stone(WHITE, event.x, event.y)

    def _place_stone(self, color, x, y):
        row, col = self.xy2rc(x, y)
        if row == -1 or col == -1:
            return

        if not self.game.is_playing() or self.game.next_move_color != color:
            return

        if not self.frame.is_human(color):
            return

        if (row, col) in self._stones:
            return

        self.game.make_move(color, row, col)

    def rc2xy(self, row: int, col: int) -> (int, int):
        return CANVAS_OFFSET + MARGIN + col * GRID_SIZE, CANVAS_OFFSET + MARGIN + row * GRID_SIZE

    def xy2rc(self, x: float, y: float) -> (int, int):
        col = int(round((x - CANVAS_OFFSET - MARGIN) / GRID_SIZE))
        row = int(round((y - CANVAS_OFFSET - MARGIN) / GRID_SIZE))
        x2, y2 = self.rc2xy(row, col)
        if abs(x2-x) > STONE_CLICK_RADIUS or abs(y2-y) > STONE_CLICK_RADIUS:
            return -1, -1
        return row, col

    def add_stone(self, color, row, col):
        assert (row, col) not in self._stones
        self._stones[(row, col)] = self._draw_circle(self.rc2xy(row, col),
                                                     STONE_RADIUS,
                                                     'black' if color == BLACK else 'white')

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

