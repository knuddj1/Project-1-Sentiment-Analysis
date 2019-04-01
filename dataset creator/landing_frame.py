from tkinter import *
from base_frame import BaseFrame


class LandingFrame(BaseFrame):
    def __init__(self, manager, size):
        BaseFrame.__init__(self, manager, size)
        top_frame = Frame(self)
        top_frame.pack(pady=20)

        self.new_btn = Button(top_frame, width=10, height=3, text="New Config", command=lambda: self.action("settings"))
        self.new_btn.pack()
        
        mid_frame = Frame(self)
        mid_frame.pack(pady=10, ipadx=10)

        self.bar=Entry(mid_frame,width=30)
        self.bar.pack(side=LEFT)

        self.bbutton= Button(mid_frame, text="Browse", command=self.browse)
        self.bbutton.pack(side=RIGHT)

        bot_frame = Frame(self)
        bot_frame.pack(ipadx=10)

        self.load_btn = Button(bot_frame, width=30, height=2, text="Load Config", command=lambda: self.action("settings", self.bar.get()))
        self.load_btn.pack(side=BOTTOM)

    def action(self, response, path=None):
        if path is not None:
            self.load(path)
        else:
            self.destroy()
            self.manager.update(response)

    def load(self, path):
        import os
        from tkinter import messagebox
        
        if len(path) is 0:
            warning_msg = "CONFIG PATH: Cannot be blank!"
            messagebox.showwarning("Warning", warning_msg)
        elif not os.path.exists(path):
            warning_msg = "CONFIG PATH: No file exists at the path: '{}'!".format(path)
            messagebox.showwarning("Warning", warning_msg)
        else:
            import json
            try:
                with open(path, 'r') as f:
                    config = json.load(f)
                    self.manager.configs = config["CONFIGS"]
                    del config["CONFIGS"]
                    self.manager.settings = config
                    self.destroy()
                    self.manager.update("settings")
            except:
                warning_msg = "CONFIG PATH: Not a valid config!"
                messagebox.showwarning("Warning", warning_msg)

    def browse(self):
        from tkinter.filedialog import askopenfilename
        Tk().withdraw() 
        self.bar.delete(0, END)
        self.bar.insert(0, askopenfilename())