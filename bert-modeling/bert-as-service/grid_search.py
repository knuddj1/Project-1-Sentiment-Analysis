import json
import numpy as np
from load_bert_data import get_data

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.losses import categorical_crossentropy


def save(model, train_results):
    results_dic = {
        'acc':       train_results['acc'],
        'loss':      train_results['loss'],
        'val_acc':   train_results['val_acc'],
        'val_loss':  train_results['val_loss'],
    }
    with open('results.json', 'w') as f:
        json.dump(results_dic, f)
    
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model.h5")
    print("Saved model to disk")
    
    

# BERT Params ##########
casing_types = ["uncased", "cased"]
embed_sizes = [768, 1024]
#######################

# Trainer Params ######
VALIDATION_SPLIT = 0.1
BATCH_SIZE = 128
NB_EPOCHS = 10
SHUFFLE = True
######################


# Grid Search Params #####
optimizers = ["sgd", "rmsprop", "adam", "adagrad", "adadelta", "adamax", "nadam"]
dense_vals = [32, 64, 128, 256, 512]
max_n_dense_layers = 10
dropout_rates = [0.1, 0.2, 0.3, 0.4, 0.5]
#########################


X, y = get_data(casing_type=  , embed_size=  )


model = Sequential()
model.compile(loss=categorical_crossentropy, optimizer='TODO', metrics=['accuracy'])
model.fit(X, y, batch_size=BATCH_SIZE, shuffle=SHUFFLE, epochs=NB_EPOCHS,  validation_split=VALIDATION_SPLIT, verbose=1)