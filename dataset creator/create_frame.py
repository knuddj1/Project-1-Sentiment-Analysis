import loader
import stats
import construct
import save
import threading
import queue
import os
from tkinter import *
from tkinter import messagebox
from base_frame import BaseFrame


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
        self.run()
        

    def run(self):
        msg_queue = queue.Queue()
        thr = threading.Thread(target=self.build_dataset, args=(msg_queue,))
        thr.start()
        self.after(2000, self.update, msg_queue)

    def update(self, msg_queue):
        try:
            msg = msg_queue.get_nowait()
            if msg is not object():
                self.textbox.config(state=NORMAL)
                self.textbox.insert(END, msg)
                self.textbox.config(state=DISABLED)
                self.after(2000, self.update, msg_queue)
            else:
            # By not calling root.after here, we allow update to
            # truly end
                pass
        except queue.Empty:
            self.after(2000, self.update, msg_queue)

    def build_dataset(self, msg_queue):
        save_func = save.get_save_func(self.final["DATASET_FILE_EXTENSION"])

        msg_queue.put("Loading datasets. This may take a while. \n")
        # Load individual datasests
        datasets = loader.load_data(self.final["CONFIGS"], msg_queue)
        msg_queue.put("Finished loading datasets! \n" + "-"*50 + "\n")
        msg_queue.put("Constructing new dataset \n")
        # Construct new dataset
        training_set, test_set = construct.get_subset(datasets, self.final)
        msg_queue.put("Finished Constructing datasets! \n" + "-"*50 + "\n")

        msg_queue.put("Saving dataset \n")
        save_path = self.get_save_path(self.final["DATASET_NAME"] + "_training_set")
        save_func(save_path, training_set)
        
        save_path = self.get_save_path(self.final["DATASET_NAME"] + "_test_set")
        save.save_multiple(test_set, save_path, save_func)
        msg_queue.put("Finished saving dataset \n" + "-"*50 + "\n")

        msg = "Do you want to save dataset statistics ?"
        if messagebox.askyesno("SAVE", msg):
            msg_queue.put("Saving dataset statistics \n")
            # Save statistics of each individual dataset
            datasets_stats = stats.generate_stats(test_set)
            save_path = self.get_save_path("test_set_stats")
            save_func(save_path, datasets_stats, fieldnames=datasets_stats[0].keys())
            msg_queue.put("Finished saving statistics \n" + "-"*50 + "\n")

        self.manager.update()


    def save_final(self):
        msg = "Do you want to save your settings and configs ?"
        if messagebox.askyesno("SAVE", msg):
            import json
            fname = "{}_{}.{}".format(self.final["DATASET_NAME"], "config", "json")
            fp = self.get_save_path(fname)
            with open(fp, "w") as f:
                json.dump(self.final, f, indent=4)


    def get_savedir(self):
        save_dir = self.final["DATASET_NAME"]
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
        return save_dir


    def get_save_path(self, fname):
        save_dir = self.get_savedir()
        return os.path.join(save_dir, fname)
        


    