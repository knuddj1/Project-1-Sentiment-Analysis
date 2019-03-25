from tkinter import *
from landing_frame import LandingFrame
from main_frame import MainFrame


LANDING_SIZE = (300, 200)
MAIN_SIZE = (800, 500)


class Manager:
    def __init__(self, root):
        """Constructor"""
        self.root = root
        self.root.withdraw()
        self.landing_frame()

    def landing_frame(self):
        LandingFrame(self, LANDING_SIZE)

    def update(self, res=None, *args):
        if res is "new":
            MainFrame(self, MAIN_SIZE)
        else:
            self.root.quit()



if __name__ == "__main__":
    root = Tk()
    app = Manager(root)
    root.mainloop()