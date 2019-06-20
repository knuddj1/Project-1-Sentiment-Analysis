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
copy_tree(model_dir_path, current_dir)