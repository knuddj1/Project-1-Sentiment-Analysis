from tkinter import *
from tkinter import messagebox
from base_frame import BaseFrame
import loader
import stats
import construct
import save  

XPAD = 5
YPAD = 5

class CreateFrame(BaseFrame):
    def __init__(self, manager, size, settings, configs):
        BaseFrame.__init__(self, manager, size)
        container = Frame(self, borderwidth=2, relief="groove")
        container.pack(padx=XPAD, pady=YPAD,fill=BOTH, expand=YES)
        self.textbox = Text(container)
        self.textbox.pack(anchor=CENTER, fill=BOTH)
        self.final = dict()
        self.final.update(settings)
        self.final['CONFIGS'] = configs
        self.save_final()
        self.create_dataset()


    def create_dataset(self):
        await save_func = save.get_save_func(self.final["DATASET_FILE_EXTENSION"])

        self.textbox.insert(END, "Loading datasets")
        # Load individual datasests
        await datasets = loader.load_data(self.final["CONFIGS"])
        self.textbox.insert(END, "Done")
        self.textbox.insert(END, "-"*50)
        self.textbox.insert(END, "Constructing new dataset")
        # Construct new dataset
        await training_set, test_set = construct.get_subset(datasets, self.final["TEST_SET_SIZE"])
        self.textbox.insert(END, "Done")
        self.textbox.insert(END, "-"*50)

        self.textbox.insert(END, "Saving dataset")
        await save_func(self.final["DATASET_NAME"] + "_training_set", training_set)
        await save.save_multiple(test_set, self.final["DATASET_NAME"] + "_test_set", save_func)
        self.textbox.insert(END, "Done")
        self.textbox.insert(END, "-"*50)

        msg = "Do you want to save dataset statistics ?"
        if messagebox.askokcancel("SAVE", msg):
            self.textbox.insert(END, "Saving dataset statistics")
            # Save statistics of each individual dataset
            await datasets_stats = stats.generate_stats(test_set)
            await save_func(self.final["DATASET_NAME"] + "_test_set_stats", datasets_stats, fieldnames=datasets_stats[0].keys())
            self.textbox.insert(END, "Done")
            self.textbox.insert(END, "-"*50)

        self.manager.update()

    def save_final(self):
        msg = "Do you want to save your settings and configs ?"
        if messagebox.askokcancel("SAVE", msg):
            import json
            fname = "{}_{}.{}".format(self.final["DATASET_NAME"], "config", ".json")
            with open(fname, "w") as f:
                json.dump(self.final, f, indent=4)

        
        


    