from tkinter import *
from base_frame import BaseFrame


class LandingFrame(BaseFrame):
    def __init__(self, manager, size):
        BaseFrame.__init__(self, manager, size)
        top_frame = Frame(self)
        top_frame.pack(pady=20)

        self.new_btn = Button(top_frame, width=10, height=3, text="New Config", command=lambda: self.action("new"))
        self.new_btn.pack()
        
        mid_frame = Frame(self)
        mid_frame.pack(pady=10, ipadx=10)

        self.bar=Entry(mid_frame,width=30)
        self.bar.pack(side=LEFT)

        self.bbutton= Button(mid_frame, text="Browse", command=self.browse)
        self.bbutton.pack(side=RIGHT)

        bot_frame = Frame(self)
        bot_frame.pack(ipadx=10)

        self.load_btn = Button(bot_frame, width=30, height=2, text="Load Config", command=lambda: self.action("load", self.bar.get()))
        self.load_btn.pack(side=BOTTOM)

    def action(self, response, path=None):
        self.destroy()
        self.manager.update(response, path)

    def browse(self):
        from tkinter.filedialog import askopenfilename
        Tk().withdraw() 
        self.bar.delete(0, END)
        self.bar.insert(0, askopenfilename())