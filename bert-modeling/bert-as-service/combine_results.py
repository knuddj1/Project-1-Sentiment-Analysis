import json
import csv
from pathlib import Path, PurePath


data_dir = 'F:/grid_search_results'
all_results = []

for filename in Path(data_dir).glob('**/results.json'):
    with open(filename, 'r') as f:
        results = json.load(f)

        model_name = str(filename).split('\\')[-2]
        model_results = {"model_name":  model_name}
        test_set_names = list(results.keys())[2:]

        for test_set in test_set_names:
            model_results[test_set] = results[test_set]
        all_results.append(model_results)

out_dir = PurePath(data_dir,'all results.csv')
keys = all_results[0].keys()

with open(out_dir, 'w', newline='') as f:
    w = csv.DictWriter(f, keys)
    w.writeheader()
    w.writerows(all_results)