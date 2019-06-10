import pandas as pd
import numpy as np
import os
import json
from bert_serving.client import BertClient

save_dir = "R:\custom"

bert = BertClient(check_length=False) 
embed_size = len(bert.encode(["test"])[0])

bert_str = "_BERT_encoded_cased_" + str(embed_size)


train_set_path = r"R:\custom\custom_training_set.csv"

test_sets_dir = r"R:\custom\custom_test_set"
dataset_paths = [os.path.join(test_sets_dir, fname) for fname in os.listdir(test_sets_dir)]


def embed_dataset(path):
    with open(path, mode="r", encoding="utf-8") as f:
        df = pd.read_csv(f)
        X = bert.encode(df["input"].tolist()).tolist()
        y = df["label"].tolist()

    return [{"input": i, "label": l} for i, l in zip(X, y)]

# Embed training set

train_save_path = os.path.join(save_dir, "custom_training_set" + bert_str + ".json")
data = embed_dataset(train_set_path)
with open(train_save_path, mode="w", encoding="utf-8") as fp:
        json.dump(data, fp,indent=4)

# Embed test set

test_set_save_dir = os.path.join(save_dir, "custom_test_set" + bert_str)

if os.path.isdir(test_set_save_dir) is not True:
    os.mkdir(test_set_save_dir)


for dpath in dataset_paths:

    filename = dpath.split('\\')[-1]
    save_name = filename.split('.')[0] + bert_str + ".json"
    fullpath = os.path.join(test_set_save_dir, save_name)

    data = embed_dataset(dpath)

    with open(fullpath, mode="w", encoding="utf-8") as fp:
        json.dump(data, fp,indent=4)