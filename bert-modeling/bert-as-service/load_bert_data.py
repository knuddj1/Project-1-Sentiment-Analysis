import json
import numpy as np
import pandas as pd
from keras.utils import to_categorical

def get_data(casing_type="uncased", embed_size=768):
    bert_path = r"R:\custom_BERT_embedded\custom_training_set_BERT_encoded_{0}_{1}.json".format(casing_type, embed_size)
    df = pd.read_json(bert_path)
    df["input"] = df["input"].apply(lambda x: np.array(x))
    X = np.asarray(df["input"].tolist())
    y = df["label"].values
    y = to_categorical(y, num_classes=3)
    return X, y 