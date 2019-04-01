import os
from tkinter import *
from base_frame import BaseFrame


XPAD = 5
YPAD = 5

 
class DataConfigFrame(BaseFrame):
    def __init__(self, manager, size):
        BaseFrame.__init__(self, manager, size)
        self.grab_set()
        container = Frame(self, borderwidth=2, relief="groove")
        container.pack(padx=XPAD, pady=YPAD,fill=BOTH, expand=YES)
        
        # Dataset Name
        f1 = Frame(container)
        f1.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        Label(f1, text="Dataset name:").pack(side=LEFT, anchor=N)
        self.e1 = Entry(f1, width=30)
        self.e1.pack(side=RIGHT, anchor=N)

        # Dataset Path
        f2 = Frame(container)
        f2.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        f2a = Frame(f2)
        f2a.pack(fill=BOTH)
        Label(f2a, text="Dataset path:").pack(side=LEFT, anchor=N)
        self.e2 = Entry(f2a, width=30)
        self.e2.pack(side= RIGHT, anchor=N)
        f2b = Frame(f2, height=20)
        f2b.pack_propagate(0)
        f2b.pack(fill=BOTH)
        Button(f2b, text="Browse", width=25, command=lambda: self.browse(self.e2)).pack(side=RIGHT,anchor=E)
        
        # Loading Script Path
        f3 = Frame(container)
        f3.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        f3a = Frame(f3)
        f3a.pack(fill=BOTH)
        Label(f3a, text="Loading script path:").pack(side=LEFT, anchor=N)
        self.e3 = Entry(f3a, width=30)
        self.e3.pack(side= RIGHT, anchor=N)
        f3b = Frame(f3, height=20)
        f3b.pack_propagate(0)
        f3b.pack(fill=BOTH)
        Button(f3b, text="Browse", width=25, command=lambda: self.browse(self.e3)).pack(side=RIGHT, anchor=E)


        # Percentage
        f4 = Frame(container)
        f4.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        Label(f4, text="Percentage of dataset to use:").pack(side=LEFT, anchor=W)
        self.e4 = Scale(f4,orient='horizontal', length=150, from_=0, to=1, resolution=-1, digits=3)
        self.e4.set(1)
        self.e4.pack(side=RIGHT, anchor=N)
        

        # Optional Parameters
        f5 = Frame(container)
        f5.pack(fill=BOTH, padx=XPAD, pady=YPAD, ipadx=30, ipady=5)
        f5a = Frame(f5)
        f5a.pack(fill=BOTH)
        Label(f5a, text="Optional loading script paramaters:").pack(side=LEFT, anchor=N)
        self.lbe1 = Entry(f5a, width=10)
        self.lbe1.pack(side=LEFT)
        Label(f5a, text=":").pack(side=LEFT)
        self.lbe2 = Entry(f5a, width=10)
        self.lbe2.pack(side=LEFT)
        Button(f5a, text="Add", command=self.add_item).pack(side=RIGHT, anchor=E)
        f5b = Frame(f5)
        f5b.pack(fill=BOTH, pady=10)
        Button(f5b, text="Delete", height=5, command=self.delete_item).pack(side=RIGHT, anchor=S)
        self.e5 = Listbox(f5b, width=23, height=5)
        self.e5.pack(side= RIGHT, anchor=E)
        sb = Scrollbar(f5b, orient="vertical")
        sb.config(command=self.e5.yview)
        sb.pack(side="right", fill="y")
        self.e5.config(yscrollcommand=sb.set)

        f6 = Frame(container)
        f6.pack(fill=BOTH, pady=10)
        Button(f6, text="Submit", height=3, command=self.submit).pack(side=BOTTOM, fill=X,  padx=10, expand=1,anchor=S)

    def add_item(self):
        if len(self.lbe1.get()) is 0 or len(self.lbe2.get()) is 0: 
            pass
        else:
            self.e5.insert(END,"{}:{}".format( self.lbe1.get(), self.lbe2.get()))
    
    def delete_item(self):
        try:
            self.e5.delete(self.e5.curselection())
        except:
            pass

    def browse(self, textbox):
        from tkinter.filedialog import askopenfilename
        Tk().withdraw() 
        textbox.delete(0, END)
        textbox.insert(0, askopenfilename())

    def load(self, dname, config):
        self.e1.insert(END, dname)
        self.e2.insert(END, config["DATASET_PATH"])
        self.e3.insert(END, config["LOADING_SCRIPT"])
        self.e4.set(config["PERCENT"])
        if config["OTHER_PARAMS"] is not None:
            for k,v in config["OTHER_PARAMS"].items():
                self.e5.insert(END, "{}:{}".format(k,v))

    def submit(self):
        if self.validate() is True:
            other_params = None
            if len(self.e5.get(0, END)) > 0:
                other_params = {p.split(":")[0]: p.split(":")[1] for p in self.e5.get(0, END)}

            config = {
                self.e1.get(): {
                    "DATASET_PATH": self.e2.get(),
                    "LOADING_SCRIPT": self.e3.get(),
                    "PERCENT": self.e4.get(),
                    "OTHER_PARAMS": other_params
                }
            }
            self.destroy()
            self.manager.add(config)

    def validate(self):
        from tkinter import messagebox

        OK = True

        if os.path.exists(self.e1.get()):
            warning_msg = "DATASET NAME:A dataset with the name {} already exists!".format(self.e1.get())
            messagebox.showwarning("Warning", warning_msg)
            OK = False

        elif not os.path.exists(self.e2.get()):
            warning_msg = "DATASET PATH: No file exists at the path: '{}'!".format(self.e2.get())
            messagebox.showwarning("Warning", warning_msg)
            OK = False

        elif not os.path.exists(self.e3.get()):
            warning_msg = "LOADING SCRIPT PATH: No file exists at the path: '{}'!".format(self.e3.get())
            messagebox.showwarning("Warning", warning_msg)
            OK = False

        return OK

