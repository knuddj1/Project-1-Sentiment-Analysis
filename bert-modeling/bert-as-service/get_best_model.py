import csv
import json
import os
from distutils.dir_util import copy_tree

best_model = None
best_score = 0

with open('all results.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader) # remove headers
    for row in csv_reader:
        model_name = row[0]
        test_results = row[1:]
        model_overall_score = sum(float(x) for x in test_results) / len(test_results)
        if model_overall_score > best_score:
            best_score = model_overall_score
            best_model = model_name


current_dir = os.path.abspath(os.path.dirname(__file__))
model_dir_path = os.path.join("F:/grid_search_results/models", best_model)
save_dir_name = "best_model"
if not os.path.isdir(save_dir_name): os.mkdir(save_dir_name)
save_dir = os.path.join(current_dir, save_dir_name)
copy_tree(model_dir_path, save_dir)