from tkinter import *
from tkinter import messagebox

class BaseFrame(Toplevel):
    def __init__(self, manager, size):
        """Constructor"""
        self.manager = manager
        Toplevel.__init__(self)

        self.resizable(width=False, height=False)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        w, h = size
        x = int((screen_width/2) - (w/2))
        y = int((screen_height/2) - (h/2))
        self.geometry("{}x{}+{}+{}".format(w, h, x, y))

        self.title("Dataset Builder")
        self.protocol("WM_DELETE_WINDOW", self.close_app)
 
    def close_app(self):
        if messagebox.askokcancel("Close", "Are you sure...?"):
            self.onClose()

    def onClose(self):
        """"""
        self.destroy()
        self.manager.update()