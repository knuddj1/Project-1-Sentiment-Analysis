import pandas
from tkinter import *
from landing_frame import LandingFrame
from main_frame import MainFrame
from settings_frame import SettingFrame
from create_frame import CreateFrame



LANDING_SIZE = (300, 200)
MAIN_SIZE = (770, 500)
SETTING_SIZE = (300, 400)
CREATE_SIZE = (500, 300)


class Manager:
    def __init__(self, root):
        """Constructor"""
        self.root = root
        self.root.withdraw()
        self.settings = None
        self.configs = None
        self.update("landing")
        

    def update(self, res=None, *args):
        if res is "landing":
            LandingFrame(self, LANDING_SIZE)
        if res is "settings":
            setting_frame = SettingFrame(self, SETTING_SIZE)
            if self.settings is not None:
                setting_frame.load(self.settings)
        elif res is "configs":
            main_frame = MainFrame(self, MAIN_SIZE)
            if self.configs is not None:
                main_frame.load(self.configs)
        elif res is "proceed":
            CreateFrame(self, CREATE_SIZE, self.settings, self.configs)
        else:
            self.root.quit()



if __name__ == "__main__":
    root = Tk()
    app = Manager(root)
    root.mainloop()