from tkinter import *
from base_frame import BaseFrame
from data_config import DataConfigFrame


XPAD = 10
YPAD = 10
DATA_CONFIG_SIZE = (400, 450)



class MainFrame(BaseFrame):
    def __init__(self, manager, size):
        BaseFrame.__init__(self, manager, size)
        topleft = Frame(self)
        topleft.pack(fill=BOTH)
        Button(topleft, text="Settings", command=self.go_back).pack(padx=XPAD, pady=YPAD, side=LEFT,anchor=W)
        Button(topleft, text="Create New Dataset", command=self.proceed).pack(padx=XPAD, pady=YPAD, side=RIGHT,anchor=E)
        self.container = Frame(self, borderwidth=2, relief="groove")
        self.container.pack(padx=XPAD, pady=YPAD,fill=BOTH, expand=YES)
        self.inner_containers = list()
        self.configs = dict()
        self.update()
        self.display()

    def add_container(self):
        inner_container = Frame(self.container)
        inner_container.pack(anchor=W)
        self.inner_containers.append(inner_container)

    def clear_containers(self):
        for container in self.inner_containers:
            container.destroy()
        self.inner_containers = list()

    def display_button(self, size, command, dname=None):
        add_frame = Frame(self.inner_containers[-1], borderwidth=2, relief="raised", width=size, height=size)
        add_frame.pack_propagate(0)
        add_frame.pack(padx=XPAD, pady=YPAD, side=LEFT, anchor=N)    
        btn = Button(add_frame, text=dname, command=command, font=('wasy10', 15), wraplength=100)
        btn.pack(fill=BOTH, anchor=CENTER, expand=True)
        if dname != "Add New Data Config":
            cmd = lambda dname=dname: self.delete(dname)
            btn = Button(add_frame, text="delete", command=cmd, font=('wasy10', 15), wraplength=100)
            btn.pack(fill=BOTH, anchor=CENTER, expand=True)

    def display(self):
        self.clear_containers()
        self.add_container()
        size = 128
        self.display_button(size, command=self.create, dname="Add New Data Config")
        n_wide = self.container.winfo_width() // (size + (XPAD + YPAD))
        for i, dname in enumerate(self.configs.keys()):
            if (i+1) % n_wide == 0:
                self.add_container()
            cmd = lambda dname=dname: self.load_config(dname)
            self.display_button(size, command=cmd, dname=dname)

    def load_config(self, dname):
        DataConfigFrame(self, DATA_CONFIG_SIZE).load(dname, self.configs[dname])

    def create(self):
        DataConfigFrame(self, DATA_CONFIG_SIZE)   

    def add(self, config):
        self.grab_release()
        self.configs.update(config)
        self.display()

    def delete(self, dname):
        from tkinter import messagebox
        msg = "Are you sure you wish to delete {} ?".format(dname)
        if messagebox.askokcancel("DELETE", msg):
            del self.configs[dname]
            self.display()

    def load(self, configs):
        self.configs = configs
        self.display()

    def go_back(self):
        self.manager.configs = self.configs
        self.manager.update("settings")
        self.destroy()

    def proceed(self):
        from tkinter import messagebox
        if len(self.configs) is not 0:
            msg = "Are you sure you're ready to create a new dataset ?"
            if messagebox.askokcancel("CREATE", msg):
                self.manager.configs = self.configs
                self.manager.update("proceed")
                self.destroy()
        else:
            warning_msg = "DATA CONFIGS: Must be at least one!"
            messagebox.showwarning("Warning", warning_msg)