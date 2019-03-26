import os
import csv
import json

def save_to_csv(save_path, dataset, fieldnames=["input", "label"]):
    """
    save_path : string - absoulute path to save dataset
    dataset : list(dict)  
    --------------------------------------------------------------------
    Saves the dataset to csv.
    Dataset should be a list of dictionaries with keys:
        -> input
        -> label
    """
    save_path += ".csv"
    with open(save_path, mode="w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)


def save_to_json(save_path, dataset):
    """
    save_path : string - absoulute path to save dataset
    dataset : list(dict)  
    --------------------------------------------------------------------
    Saves the dataset to json.
    Dataset should be a list of dictionaries with keys:
        -> input
        -> label
    """
    save_path += ".json"
    with open(save_path, mode="w", encoding="utf-8") as f:
        json.dump(dataset, f)


def save_multiple(datasets, save_dir, save_func):
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)

    for dname, dataset in datasets.items():
        save_path = os.path.join(save_dir, dname)
        save_func(save_path, dataset)


def get_save_func(file_ext):
    if file_ext is "csv":
        return save_to_csv
    elif file_ext is "json":
        return save_to_json
    else:
        raise ValueError("File extension for formatted dataset must be either csv or json")
