import json
import os
import importlib.util

path = "data_configs.json"

configs = json.load(open(path))

for dataset_name in configs.keys():
    
    data_config = configs[dataset_name]

    if data_config["use"]:

        spec = importlib.util.spec_from_file_location(dataset_name, data_config["loading_script"])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if data_config["extra_params"] is not None:
                data = module.load(data_config["dataset_path"], data_config["extra_params"])
        else:
                data = module.load(data_config["dataset_path"]) 