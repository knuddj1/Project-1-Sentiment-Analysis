from tkinter import *
from base_frame import BaseFrame


XPAD = 5
YPAD = 5

class SettingFrame(BaseFrame):
    def __init__(self, manager, size):
        BaseFrame.__init__(self, manager, size)
        
        container = Frame(self, borderwidth=2, relief="groove")
        container.pack(padx=XPAD, pady=YPAD,fill=BOTH, expand=YES)

        f1 = Frame(container)
        f1.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        Label(f1, text="Dataset name:").pack(side=LEFT, anchor=N)
        self.e1 = Entry(f1, width=30)
        self.e1.pack(side=RIGHT, anchor=N)

        f3 = Frame(container)
        f3.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        Label(f3, text="Dataset File Extension:").pack(side=LEFT, anchor=N)
        self.e3 = StringVar()
        self.e3.set("csv")
        Radiobutton(f3, variable=self.e3, value="csv").pack(side=RIGHT, anchor=N)
        Label(f3, text="CSV").pack(side=RIGHT, anchor=N)
        Radiobutton(f3, variable=self.e3, value="json").pack(side=RIGHT, anchor=N)
        Label(f3, text="JSON").pack(side=RIGHT, anchor=N)

        f4 = Frame(container)
        f4.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        Label(f4, text="Test set size:").pack(side=LEFT, anchor=W)
        self.e4 = Scale(f4,orient='horizontal', length=100, from_=0, to=0.5, resolution=-1, digits=2)
        self.e4.set(0)
        self.e4.pack(side=RIGHT, anchor=N)

        
        f5 = Frame(container)
        f5.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        self.e5 = BooleanVar()
        Label(f5, text="Shuffle Dataset").pack(side=LEFT, anchor=N)
        Checkbutton(f5, variable=self.e5).pack(side=LEFT, anchor=N)

        f6 = Frame(container)
        f6.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        Label(f6, text="Number shuffles:").pack(side=LEFT, anchor=W)
        self.e6 = Spinbox(f6, width=5, from_=0, to=10)
        self.e6.pack(side=RIGHT, anchor=N)


        f7 = Frame(container)
        f7.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        Button(f7, text="Proceed", command=self.proceed).pack(side=BOTTOM, anchor=S)
    
    def proceed(self):
        if self.validate(self.e1.get()):
            settings = {
                "DATASET_NAME" : self.e1.get(),
                "DATASET_FILE_EXTENSION" : self.e3.get(),
                "TEST_SET_SIZE" : self.e4.get(),
                "SHUFFLE" : self.e5.get(),
                "NUM_SHUFFLES" : self.e6.get()
            }
            self.destroy()
            self.manager.settings = settings
            self.manager.update("configs")

    def validate(self, dname):
        import glob
        from tkinter import messagebox
        if len(glob.glob(dname + ".*")) is not 0:
            warning_msg = "Dateset Name: A dataset with the name '{}' already exists!".format(dname)
            messagebox.showwarning("Warning", warning_msg)
            return False
        return True

    def load(self, settings):
        self.e1.insert(END, settings["DATASET_NAME"])
        self.e3.set(settings["DATASET_FILE_EXTENSION"])
        self.e4.set(settings["TEST_SET_SIZE"])
        self.e5.set(settings["SHUFFLE"])
        self.e6.delete(0, "end")
        self.e6.insert(0, settings["NUM_SHUFFLES"])