import json
import numpy as np
from keras.models import model_from_json
from gensim.parsing.preprocessing import *
from keras.preprocessing.sequence import pad_sequences

CUSTOM_FILTERS = [  lambda x: x.lower(), #To lowercase
                    lambda text: re.sub(r'https?:\/\/.*\s', '', text, flags=re.MULTILINE), #To Strip away URLs
                    strip_tags, #Remove tags from s using RE_TAGS.
                    strip_non_alphanum,#Remove non-alphabetic characters from s using RE_NONALPHA.
                    strip_punctuation, #Replace punctuation characters with spaces in s using RE_PUNCT.
                    strip_numeric, #Remove digits from s using RE_NUMERIC.
                    strip_multiple_whitespaces,#Remove repeating whitespace characters (spaces, tabs, line breaks) from s and turns tabs & line breaks into spaces using RE_WHITESPACE.
                    remove_stopwords, # Set of 339 stopwords from Stone, Denis, Kwantes (2010).
                    lambda x: strip_short(x, minsize=3), #Remove words with length lesser than minsize from s.
                ]

MAX_SIZE = 500
NUM_CATEGORIES = 3

def prepare_labels(arr):
    n_samples = len(arr)
    y = np.zeros(shape=(n_samples, NUM_CATEGORIES))
    for i in range(n_samples):
        label = int(arr[i])
        y[i, label+1] = 1.
    return y
    

def prepare(X, y):
    X_prepared = pad_sequences(X, maxlen=MAX_SIZE, truncating='post', padding='pre')
    y_prepared = prepare_labels(y)
    return X_prepared, y_prepared


def get_test_data(vocab, df):
    data = []
    labels = []

    for _, r in df.iterrows():
        words = preprocess_string(r['input'], CUSTOM_FILTERS)
        nums = [0] * len(words)
        for i, word in enumerate(words):
            if word in vocab:
                nums[i] = vocab[word]
        data.append(nums)
        labels.append(r['label'])
            
    x_test, y_test = prepare(data, labels)

    return x_test, y_test
    

class OwnModel:
    def __init__(self, m_path, w_path, voc_path):
        self.model = self._get_model(m_path, w_path)
        self.vocab = self._get_vocab(voc_path)
        self.__name__ = "OwnModel"

    def __call__(self, df):
        x_test, y_test = get_test_data(self.vocab, df) 
        _, test_acc = self.model.evaluate(x_test,y_test)
        return test_acc
        
    def _get_model(self, model_path, weights_path):
        json_file = open(model_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(weights_path)
        #evaluate loaded model on test data
        loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return loaded_model

    def _get_vocab(self, vocab_path):
        with open('word_to_index_top_30000.json', 'r') as f:
            vocab = json.load(f)
        return vocab