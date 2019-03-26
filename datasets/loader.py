import json
import csv
import importlib.util
import os
import glob


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


def load_data(configs, save_func):
    """
    configs : list(dict) - configuration file for each dataset located in data_configs.py
    file_ext : str - 
    --------------------------------------------------------------------
    output : dict - All datasets concatenated in format {dataset_name:{"input":x,"label":x}}
    --------------------------------------------------------------------
    TODO
    """
    current_dir = os.path.dirname(__file__)

    dataset = dict()

    formatted_dir = os.path.join(current_dir, "formatted_datasets")

    if not os.path.isdir(formatted_dir):
        os.mkdir(formatted_dir)

    loading_scripts_dir = os.path.join(current_dir, "loading_scripts")

    for dataset_name in configs.keys():
        data_config = configs[dataset_name]

        if data_config["use"]:
            print("Currently loading dataset: '%s'" % dataset_name)
            formatted_fpath_no_ext = os.path.join(formatted_dir, dataset_name)
            
            fpath = glob.glob(formatted_fpath_no_ext + ".*")
            if len(fpath) is not 0:
                dataset[dataset_name] = retrieve_dataset(fpath[0])
            else:
                print("This dataset has not been formatted. It will be formatted now. This may take a while.")
                dataset[dataset_name] = extract_dataset(loading_scripts_dir, data_config)
                save_func(formatted_fpath_no_ext, dataset[dataset_name])
                print("Formatting complete.")
            print("Done. \n")

    print("Finished loading! - Using {}/{} available datasets: \n".format(len(dataset.keys()), len(configs.keys())))
    for n, dname in enumerate(configs.keys()):
        out_str = "{}. {}".format(n + 1, dname)
        if dname in dataset.keys():    
            out_str = out_str + " <=="
        print(out_str)
    print("\n")
    return dataset




