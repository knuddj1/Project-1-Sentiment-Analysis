import json
import importlib.util
import os
from . import loader_config


def load_dataset(path, config):
    script_path = os.path.join(path, config["loading_script"])
    spec = importlib.util.spec_from_file_location("module", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # if config["extra_params"] is not None:
    #     data = module.load(config["dataset_path"], config["extra_params"])
    # else:
    #     data = module.load(config["dataset_path"])
    #
    # return data


def get_data():
    dir_name = os.path.basename(os.path.dirname(__file__))
    config_path = os.path.join(dir_name, "data_configs.json")

    configs = json.load(open(config_path))

    dataset = dict()

    formatted_dir = os.path.join(dir_name, "formatted datasets")

    if not os.path.isdir(formatted_dir):
        os.mkdir(formatted_dir)

    loading_scripts_dir = os.path.join(dir_name, "processing scripts")

    for dataset_name in configs.keys():
        data_config = configs[dataset_name]

        if data_config["use"]:
            formated_dataset_path = os.path.join(formatted_dir,'{}.{}'.format(dataset_name, loader_config.DATASET_FILE_EXTENSION))

            if os.path.exists(formated_dataset_path):
                print("Already exists")
            else:
                with open(formated_dataset_path, 'w') as f:
                    f.write("worked")
                load_dataset(loading_scripts_dir, data_config)

