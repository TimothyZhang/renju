from tkinter import Tk, Canvas, Button, GROOVE, Frame, RIGHT

# from PIL import Image, ImageTk
from renju.rule import BOARD_ROWS, BOARD_COLS, BLACK

MARGIN = 10
GRID_SIZE = 40
LINE_WIDTH = 1
assert BOARD_COLS == BOARD_ROWS

LINE_LENGTH = (BOARD_COLS - 1) * GRID_SIZE + LINE_WIDTH
BOARD_SIZE = LINE_LENGTH + MARGIN * 2

DOT_RADIUS = 3
# fixme: I have to put a offset, otherwise the board is not in the center of canvas.
CANVAS_OFFSET = 3


class Board(object):
    def __init__(self, window):
        self.canvas = Canvas(window.frame, width=BOARD_SIZE, height=BOARD_SIZE, bg='#ddaa22', bd=0)
        self.canvas.pack()

        self._draw_board()

    def _draw_board(self):
        c = self.canvas
        top = left = MARGIN + CANVAS_OFFSET
        bottom, right = top + LINE_LENGTH, left + LINE_LENGTH

        # horizontal lines
        y = top
        for row in range(BOARD_ROWS):
            c.create_line(left, y, right, y)
            y += GRID_SIZE

        # vertical lines
        x = left
        for col in range(BOARD_COLS):
            c.create_line(x, top, x, bottom)
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
            x, y = self.rc2xy(row, col)
            c.create_oval((x - DOT_RADIUS, y - DOT_RADIUS, x + DOT_RADIUS, y + DOT_RADIUS), fill='black')

    def rc2xy(self, row: int, col: int):
        return CANVAS_OFFSET + MARGIN + col * GRID_SIZE, CANVAS_OFFSET + MARGIN + row * GRID_SIZE

        # # bg
        # image = Image.open("images/board.jpg")
        # image = image.resize((512, 512), resample=Image.BICUBIC)
        # self.bg_image = photo_image = ImageTk.PhotoImage(image)
        # self.canvas.create_image((0, 0), anchor=NW, image=photo_image)

        # line = self.canvas.create_line(0, 0, 200, 100)
        # self.canvas.itemconfig(line, tags=('haha', 'hehe'))
        # self.canvas.addtag_withtag("blabla", "haha")
        # self.canvas.gettags(line)
        # self.canvas.find_withtag('haha')

    # def on_stone_clicked(self, event):
    #     canvas = event.widget
    #     x = canvas.canvasx(event.x)
    #     y = canvas.canvasy(event.y)
    #     canvas.find_closest(x, y)


class Window(object):
    def __init__(self, app):
        self.frame = Frame(app.root)
        self.frame.pack()

        self.board = Board(self)

        btn = Button(self.frame, name='test', text='TEST', fg='red', relief=GROOVE)
        btn.config(command=btn.flash)
        btn.pack(side=RIGHT)
        btn.flash()


class App(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("Renju")

        self.frame = Window(self)

    def start(self):
        # bring to front
        self.root.lift()
        self.root.call('wm', 'attributes', '.', '-topmost', True)
        self.root.after_idle(self.root.call, 'wm', 'attributes', '.', '-topmost', False)
        self.root.geometry('800x600')
        # root.iconbitmap('spider_128px_1169260_easyicon.net.ico')

        self.root.mainloop()

if __name__ == '__main__':
    App().start()
