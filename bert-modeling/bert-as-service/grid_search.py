import json
import numpy as np
import itertools
import os
from load_bert_data import get_data
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
    
########## Grid Search Parameters #########################
embed_sizes = [768, 1024] # BERT encoding  size
validation_splits = [0.1, 0.2]
batch_sizes = [64, 128, 256]
optimizers = ["sgd", "rmsprop", "adam"]
dropout_rates = [0.1, 0.2, 0.3, 0.4, 0.5]


### Generating all possible model layers ##
dense_vals = [Dense(32), Dense(64), Dense(128), Dense(256)]
max_n_dense_layers = 4
layers = []

for i in range(1, max_n_dense_layers + 1):
    nl = [dense_vals]*i
    variations = list(itertools.product(*nl))
    layers += variations
#####################################

NB_EPOCHS = 5
SHUFFLE = True

### Creating gridsearch iterator 
combinations = itertools.product(validation_splits, batch_sizes, optimizers, dropout_rates, layers)
########################################################


### Verify path to save is correct
save_dir = "R:\grid_search_results"
if os.path.isdir(save_dir): os.mkdir(save_dir)
model_save_dir = os.path.join(save_dir, "models")
if os.path.isdir(model_save_dir): os.mkdir(model_save_dir)


for e in embed_size:
    X, y, test_sets = get_data(embed_size=e)

    for vs, bs, opt, do, lc in combinations:
        model = Sequential()
        dense_layers_string = ""
        for l in lc:
            model.add(l)
            model.add(Dropout(do))
            dense_layers_string += "D-{0}".format(l.units)
        model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=['accuracy'])
        train_results = model.fit(X, y, batch_size=bs, shuffle=SHUFFLE, epochs=NB_EPOCHS,  validation_split=vs, verbose=1)

        test_results = dict()
        for dname, dset in test_sets.items():
            test_results[dname] = model.evaluate(dset["X_test"], dset["y_test"])

        model_save_path = "E-{0} VS-{1} BS-{2} OPT-{3} DO-{4} {5}".format(e, vs, bs, opt, do, dense_layers_string)
        os.mkdir(model_save_path)

        results_dic = {
            'acc':       train_results['acc'],
            'val_acc':   train_results['val_acc'],
        }

        for dname, acc in test_results.items():
            results_dic[dname] = acc

        with open(os.path.join(model_save_path,'results.json'), 'w') as f:
            json.dump(results_dic, f)
        
        model_json = model.to_json()
        with open(os.path.join(model_save_path,"model.json"), "w") as json_file:
            json_file.write(model_json)
        model.save_weights(os.path.join(model_save_path,"model.h5"))

        model_params = {
            "optimizer": opt,
            "loss_function": "categorical_crossentropy"
        }

        with open(os.path.join(model_save_path,"model_params.json"), 'w') as f:
            json.dump(results_dic, f)

        