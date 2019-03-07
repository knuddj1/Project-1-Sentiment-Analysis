import json
import os

path = "data_configs.json"

configs = json.load(open(path))

for dataset_name in configs.keys():
    data_config = configs[dataset_name]
    if data_config["use"]:
        import importlib.util
        spec = importlib.util.spec_from_file_location(dataset_name, data_config["loading_script"])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.load(data_config["dataset_path"])