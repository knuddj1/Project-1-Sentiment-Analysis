from tkinter import *
from tkinter import messagebox
from base_frame import BaseFrame


class CreateFrame(BaseFrame):
    def __init__(self, manager, size, settings, configs):
        BaseFrame.__init__(self, manager, size)

        final = dict()
        final.update(settings)
        final['CONFIGS'] = configs

        msg = "Do you want to save your settings and configs ?"
        if messagebox.askokcancel("SAVE", msg):
            import json
            fname = "{}_{}.{}".format(settings["DATASET_NAME"], "config", ".json")

            print(final)
            with open(fname, "w") as f:
                json.dump(final, f, indent=4)