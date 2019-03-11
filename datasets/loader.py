import json
import csv
import importlib.util
import os
from .settings import *


def extract_dataset(path, config):
    script_path = os.path.join(path, config["loading_script"])
    spec = importlib.util.spec_from_file_location("module", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if config["other_params"] is not None:
        data = module.load(config["dataset_path"], **config["other_params"])
    else:
        data = module.load(config["dataset_path"])
    return data


def save_to_csv(save_path, dataset):
    with open(save_path, mode="w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["input", "label"])
        writer.writeheader()
        writer.writerows(dataset)


def save_to_json(save_path, dataset):
    with open(save_path, mode="w", encoding="utf-8") as f:
        json.dump(dataset, f)


def format_dataset(data_config, script_dir, formatted_set_path):
    data = extract_dataset(script_dir, data_config)

    if DATASET_FILE_EXTENSION is "csv":
        save_to_csv(formatted_set_path, data)
    elif DATASET_FILE_EXTENSION is "json":
        save_to_json(formatted_set_path, data)
    else:
        raise ValueError("File extension for formatted dataset must be either csv or json")
    return data


def retrieve_dataset(path):
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
    current_dir = os.path.basename(os.path.dirname(__file__))
    config_path = os.path.join(current_dir, "data_configs.json")

    configs = json.load(open(config_path))

    dataset = dict()

    formatted_dir = os.path.join(current_dir, "formatted_datasets")

    if not os.path.isdir(formatted_dir):
        os.mkdir(formatted_dir)

    loading_scripts_dir = os.path.join(current_dir, "loading_scripts")

    n_used = 0

    for dataset_name in configs.keys():
        data_config = configs[dataset_name]

        if data_config["use"]:
            print("Currently loading dataset: '%s'" % dataset_name)
            n_used += 1
            dataset_proper_name = '{}.{}'.format(dataset_name, DATASET_FILE_EXTENSION)
            formatted_dataset_path = os.path.join(formatted_dir, dataset_proper_name)

            if os.path.exists(formatted_dataset_path):
                dataset[dataset_name] = retrieve_dataset(formatted_dataset_path)
            else:
                print("This dataset is not formatted. It will be formatted now. This will take longer.")
                dataset[dataset_name] = format_dataset(data_config, loading_scripts_dir, formatted_dataset_path)
                print("Formatting complete.")
            print("Done.")

    print("Finished loading! - Using {}/{} available datasets: \n".format(n_used, len(configs.keys())))
    for dname in dataset.keys():
        print("\t -> {}".format(dname))
    print()
    return dataset




