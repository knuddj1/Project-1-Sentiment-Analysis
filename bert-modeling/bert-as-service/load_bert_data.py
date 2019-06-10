import json
import numpy as np
import pandas as pd
import os
from keras.utils import to_categorical

def load_and_process(path):
    df = pd.read_json(path)
    df["input"] = df["input"].apply(lambda x: np.array(x))
    X = np.asarray(df["input"].tolist())
    y = df["label"].values
    y = to_categorical(y, num_classes=3)
    return X, y


def get_data(embed_size):
    train_path = r"R:\custom bert encoded\custom_training_set_BERT_encoded_uncased_{0}.json".format(embed_size)
    X_train, y_train = load_and_process(train_path)

    test_dir = r"R:\custom bert encoded\custom_test_set_BERT_encoded_uncased_{0}".format(embed_size)
    test_fpaths = [os.path.join(test_dir, fpath) for fpath in os.listdir(test_dir)]
    test_sets = dict()

    for fpath in test_fpaths:
        dataset_name = fpath.split("\\")[-1].split("_")[0]
        X_test, y_test = load_and_process(fpath)
        test_sets[dataset_name] = {"X_test": X_test, "y_test": y_test}

    return X_train, y_train, test_sets
