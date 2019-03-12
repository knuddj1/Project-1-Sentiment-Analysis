import json
import csv
import importlib.util
import os
from datasets.settings import *
from . import data_configs


def extract_dataset(path, config):
    """
    path : string - the current location of the loader script. 
    config : dict - dataset configuration file
    --------------------------------------------------------------------
    output: dict - singular dataset in format {"input":x,"label":x}
    --------------------------------------------------------------------
    Uses the loading script from the supplied data config to retrieve
    the dataset from its location.
    dataset returned from loading script should be a list of dictionaries
    with keys:
        -> input
        -> label
    """
    script_path = os.path.join(path, config["loading_script"])
    spec = importlib.util.spec_from_file_location("module", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    dataset_path = os.path.join(config["dataset_path"], config["dataset_filename"])

    if config["other_params"] is not None:
        data = module.load(dataset_path, **config["other_params"])
    else:
        data = module.load(dataset_path)
    return data


def save_to_csv(save_path, dataset):
    """
    save_path : string - absoulute path to save dataset
    dataset : list(dict)  
    --------------------------------------------------------------------
    Saves the dataset to csv.
    Dataset should be a list of dictionaries with keys:
        -> input
        -> label
    """
    with open(save_path, mode="w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["input", "label"])
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
    with open(save_path, mode="w", encoding="utf-8") as f:
        json.dump(dataset, f)


def format_dataset(data_config, script_dir, formatted_save_dir):
    """
    data_config : dict - loading information for a dataset
    script_dir : string - location of dataset loading scripts
    formatted_save_dir : string - directory to save formatted dataset in
    --------------------------------------------------------------------
    output : dict - singular dataset in format {"input":x,"label":x}
    --------------------------------------------------------------------
    """
    data = extract_dataset(script_dir, data_config)

    if DATASET_FILE_EXTENSION is "csv":
        save_to_csv(formatted_save_dir, data)
    elif DATASET_FILE_EXTENSION is "json":
        save_to_json(formatted_save_dir, data)
    else:
        raise ValueError("File extension for formatted dataset must be either csv or json")
    return data


def retrieve_dataset(path):
    """
    path : string - path to formatted dataset
    --------------------------------------------------------------------
    output : singular dataset in format {"input":x,"label":x}
    --------------------------------------------------------------------
    retrieves a preformatted dataset
    """
    try:
        data_file = open(path, mode="r", encoding="utf-8")
        if path.endswith(".csv"):
            import pandas as pd
            df = pd.read_csv(data_file)
            return df.to_dict('records')
        elif path.endswith(".json"):
            return json.load(data_file)
    except ValueError:
        raise ValueError("Supported file types are csv and json")


def load_data():
    """
    output : dict - All datasets concatenated in format {dataset_name:{"input":x,"label":x}}
    --------------------------------------------------------------------
    TODO
    """
    current_dir = os.path.dirname(__file__)
    
    configs = data_configs.CONFIGS

    dataset = dict()

    formatted_dir = os.path.join(current_dir, "formatted_datasets")

    if not os.path.isdir(formatted_dir):
        os.mkdir(formatted_dir)

    loading_scripts_dir = os.path.join(current_dir, "loading_scripts")

    for dataset_name in configs.keys():
        data_config = configs[dataset_name]

        if data_config["use"]:
            print("Currently loading dataset: '%s'" % dataset_name)
            dataset_proper_name = '{}.{}'.format(dataset_name, DATASET_FILE_EXTENSION)
            formatted_dataset_path = os.path.join(formatted_dir, dataset_proper_name)

            if os.path.exists(formatted_dataset_path):
                dataset[dataset_name] = retrieve_dataset(formatted_dataset_path)
            else:
                print("This dataset has not been formatted. It will be formatted now. This may take a while.")
                dataset[dataset_name] = format_dataset(data_config, loading_scripts_dir, formatted_dataset_path)
                print("Formatting complete.")
            print("Done. \n")

    print("Finished loading! - Using {}/{} available datasets: \n".format(len(dataset.keys()), len(configs.keys())))
    for n, dname in enumerate(configs.keys()):
        out_str = "\t {}. {}".format(n + 1, dname)
        if dname in dataset.keys():    
            out_str = out_str + " <=="
        else:
            out_str = out_str + " ><"
        print(out_str)
    print("\n")
    return dataset




