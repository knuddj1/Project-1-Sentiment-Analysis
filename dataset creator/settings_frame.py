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
        self.e5.set(True)
        Label(f5, text="Shuffle Dataset").pack(side=LEFT, anchor=N)
        Checkbutton(f5, variable=self.e5).pack(side=LEFT, anchor=N)

        f6 = Frame(container)
        f6.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        Label(f6, text="Number shuffles:").pack(side=LEFT, anchor=W)
        self.e6 = IntVar()
        self.e6.set(1)
        Spinbox(f6, width=5, textvariable=self.e6, from_=0, to=10).pack(side=RIGHT, anchor=N)

        f7 = Frame(container)
        f7.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        f7a = Frame(container)
        f7a.pack(fill=BOTH)
        Label(f7a, text="Dataset Concatenation Type:").pack(side=LEFT, anchor=N)
        f7b = Frame(container)
        f7b.pack(fill=BOTH)
        self.e7 = StringVar()
        self.e7.set("equal")
        Label(f7b, text="EQUAL").pack(side=LEFT, anchor=S)
        Radiobutton(f7b, variable=self.e7, value="equal").pack(side=LEFT, anchor=S)
        Label(f7b, text="PERCENTAGE").pack(side=LEFT, anchor=S)
        Radiobutton(f7b, variable=self.e7, value="percentage").pack(side=LEFT, anchor=S)

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
                "NUM_SHUFFLES" : self.e6.get(),
                "CONCAT_TYPE" : self.e7.get()
            }
            self.destroy()
            self.manager.settings = settings
            self.manager.update("configs")

    def validate(self, dname):
        import glob
        from tkinter import messagebox
        
        if len(dname) is 0:
            warning_msg = "DATASET NAME: Cannot be blank!"
            messagebox.showwarning("Warning", warning_msg)
            return False
        elif len(glob.glob(dname + ".*")) is not 0:
            warning_msg = "DATASET NAME: A dataset with the namse '{}' already exists!".format(dname)
            messagebox.showwarning("Warning", warning_msg)
            return False
        return True

    def load(self, settings):
        self.e1.insert(END, settings["DATASET_NAME"])
        self.e3.set(settings["DATASET_FILE_EXTENSION"])
        self.e4.set(settings["TEST_SET_SIZE"])
        self.e5.set(settings["SHUFFLE"])
        self.e6.set(settings["NUM_SHUFFLES"])
        self.e7.set(settings["CONCAT_TYPE"])