import json
import csv
import importlib.util
import os
import glob


def extract_dataset(config):
    """
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
    spec = importlib.util.spec_from_file_location("module", config["LOADING_SCRIPT"])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if config["OTHER_PARAMS"] is not None:
        data = module.load(config["DATASET_PATH"], **config["OTHER_PARAMS"])
    else:
        data = module.load(config["DATASET_PATH"])
    return data


def load_data(configs, msg_queue):
    """
    configs : dict - configuration file for each dataset
    --------------------------------------------------------------------
    output : dict - All datasets concatenated in format {dataset_name:{"input":x,"label":x}}
    --------------------------------------------------------------------
    TODO
    """
    dataset = dict()
    for i, dataset_name in enumerate(configs.keys()):
        msg_queue.put("Currently loading dataset {}/{} -> '{}' \n".format(i + 1, len(configs.keys()),dataset_name))
        data_config = configs[dataset_name]
        dataset[dataset_name] = extract_dataset(data_config)
        msg_queue.put("Finshed! \n")
    return dataset




