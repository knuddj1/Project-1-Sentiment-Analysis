import os
import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from own_model import OwnModel


def textblob_naivebayes(df):
    labels = {"pos": 1, "neg": -1}
    analyzer=NaiveBayesAnalyzer()
    outputs = df['input'].apply(lambda x: TextBlob(x, analyzer=analyzer).sentiment.classification)
    correct = 0
    for label, output in zip(df["label"], outputs):
        if label == labels[output]: correct += 1
    return correct / len(df)

def textblob_pattern(df):
    labels = [-1, 0 , 1]
    analyzer=PatternAnalyzer()
    outputs = df['input'].apply(lambda x: TextBlob(x, analyzer=analyzer).sentiment.polarity)
    correct = 0
    for label, output in zip(df["label"], outputs):
        output = min(labels, key=lambda x:abs(x-output))
        if label == output: correct += 1
    return correct / len(df)


def vader(df):
    labels = {"pos": 1, "neu": 0, "neg": -1}
    analyzer = SentimentIntensityAnalyzer()
    outputs = df['input'].apply(lambda x: analyzer.polarity_scores(x))
    correct = 0
    for label, output in zip(df["label"], outputs):
        del output['compound']
        output = max(output, key=output.get)
        if labels[output] == label: correct += 1
    return correct / len(df)


model_path = "model.json"
weights_path = "model.h5"
vocab_path = "word_to_index_top_30000.json"
testdir = "custom_test_set"

test_datasets = os.listdir(testdir)

classifiers = [textblob_naivebayes, textblob_pattern, vader, OwnModel(model_path, weights_path, vocab_path)]

results = dict()
for classifier in classifiers:
    results[classifier.__name__] = {
       dataset_file.split('.')[0]: None for dataset_file in test_datasets
    }

for dataset_file in test_datasets:
    dataset_name = dataset_file.split('.')[0]
    abs_path = os.path.join(testdir, dataset_file)
    df = pd.read_csv(abs_path)
    for classifier in classifiers:
        results[classifier.__name__][dataset_name] = classifier(df)

outlst = list()
for k, d in results.items():
    total = 0
    for key, v in d.items():
        total += v
    total /= len(d.keys())
    d.update({"overall": total})
    d.update({"classifier" : k})
    outlst.append(d)


import csv
with open("baseline_results.csv", mode="w", encoding="utf-8", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=outlst[0].keys())
    writer.writeheader()
    writer.writerows(outlst)