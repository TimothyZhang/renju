from tkinter import Tk
from renju.gui.main_frame import MainFrame


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Renju")

        self.main_frame = MainFrame(self)
        self.main_frame.pack()

    def start(self):
        # bring to front
        self.lift()
        self.call('wm', 'attributes', '.', '-topmost', True)
        self.after_idle(self.call, 'wm', 'attributes', '.', '-topmost', False)
        self.geometry('800x600')
        # root.iconbitmap('spider_128px_1169260_easyicon.net.ico')

        self.mainloop()

if __name__ == '__main__':
    App().start()
