import json
import urllib

path = "data_configs1.json"

configs = json.load(open(path))

for dataset_name in configs.keys():
    change = False
    data_config = configs[dataset_name]
    if data_config['use']:
        data_config['path'] = "Test"
        change = True
    if change:
        json.dump(configs, open(path, "w"), indent=4)

