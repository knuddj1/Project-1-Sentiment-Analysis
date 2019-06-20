import json
import numpy as np
import itertools
import os
import time
import datetime
from load_bert_data import get_data
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import backend as K

# Suppress Debug info
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
    
########## Grid Search Parameters #########################
embed_sizes = [768, 1024] # BERT encoding  size
validation_splits = [0.1, 0.2]
batch_sizes = [64, 128, 256]
optimizers = ["sgd", "rmsprop", "adam"]
dropout_rates = [0.1, 0.2, 0.3, 0.4]
activations = ["relu", "tanh", "sigmoid"]


### Generating all possible model layers ##
dense_vals = [32, 64, 128, 256]
max_n_dense_layers = 3
layers = []

for i in range(1, max_n_dense_layers + 1):
    nl = [dense_vals]*i
    variations = list(itertools.product(*nl))
    layers += variations
#####################################

NB_EPOCHS = 5
SHUFFLE = True

### Creating gridsearch iterator 
combinations = list(itertools.product(validation_splits, batch_sizes, optimizers, dropout_rates, activations, layers))
########################################################


### Verify path to save is correct
save_dir = "F:\grid_search_results"
if not os.path.isdir(save_dir): os.mkdir(save_dir)
model_save_dir = os.path.join(save_dir, "models")
if not os.path.isdir(model_save_dir): os.mkdir(model_save_dir)

start = time.time()
n_trained = 0
total_trained = 0
all_results = {}
average = 1

for e in embed_sizes:
    load_time = time.time()
    X, y, test_sets = get_data(embed_size=e)
    start = start + (time.time() - load_time)

    for vs, bs, opt, do, act, dls in combinations:

        dense_layers_string = ""
        for dl in dls:
            dense_layers_string += "D-{0}".format(dl)
        
        model_name = "E-{0} VS-{1} BS-{2} OPT-{3} DO-{4} ACT-{5} {6}".format(e, vs, bs, opt, do, act, dense_layers_string)
        model_save_path = os.path.join(model_save_dir, model_name)


        ### Useful For resuming training
        if not os.path.isdir(model_save_path):
            os.mkdir(model_save_path)

            os.system('cls')
            print("{0}/{1} Models Trained!".format(n_trained, len(combinations) * 2))
            print("Total Time elapsed: {0}".format(round(time.time()-start, 2)))
            if total_trained > 0:
                average = round((time.time()-start) / total_trained, 2)
                print("Average Model Training Time: {0}".format(average))
            estimate = datetime.timedelta(seconds=((len(combinations) * 2) - n_trained) * average)
            print("Estimated Completion Time: {0}".format(estimate))
            print("================================")
            print("Current Model Parameters:")
            print("  => Validation Split: {0} ".format(vs))
            print("  => Batch Size: {0} ".format(bs))
            print("  => Optimizer: {0} ".format(opt))
            print("  => Dropout Percentage: {0} ".format(do))
            print("  => Activation Function: {0} ".format(act))
            print("  => Dense Layers: {0}".format('|'.join(str(x) for x in dls)))

            model = Sequential()
            dense_layers_string = ""
            for n, dl in enumerate(dls):
                if n == 0:
                    model.add(Dense(dl, activation=act, input_shape=(X.shape[-1],)))
                else:
                    model.add(Dense(dl, activation=act))
                model.add(Dropout(do))
                dense_layers_string += "D-{0}".format(dl)
            model.add(Dense(3, activation="softmax"))
            model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=['accuracy'])
            history = model.fit(X, y, batch_size=bs, shuffle=SHUFFLE, epochs=NB_EPOCHS,  validation_split=vs, verbose=0)

            test_results = dict()
            for dname, dset in test_sets.items():
                test_results[dname] = model.evaluate(dset["X_test"], dset["y_test"], verbose=0)[1]

            results_dic = {
                'acc': history.history['acc'],
                'val_acc': history.history['val_acc'],
            }

            for dname, acc in test_results.items():
                results_dic[dname] = acc
				
			all_results[model_name] = results_dic

            with open(os.path.join(model_save_path,'results.json'), 'w') as f:
                json.dump(results_dic, f, indent=4)
            
            model_json = model.to_json()
            with open(os.path.join(model_save_path,"model.json"), "w") as json_file:
                json_file.write(model_json)
            model.save_weights(os.path.join(model_save_path,"model.h5"))

            compile_params = {
                "optimizer": opt,
                "loss_function": "categorical_crossentropy"
            }

            with open(os.path.join(model_save_path,"compile_params.json"), 'w') as f:
                json.dump(compile_params, f, indent=4)
            

            ## Clear memory
            del model
            del compile_params
            del model_json
            del test_results
            del history

            if K.backend() == 'tensorflow':
                K.clear_session()

            total_trained += 1

        del model_name
        del model_save_path
        del dense_layers_string

        n_trained += 1

### Saving all results
with open(os.path.join(save_dir, "results.json"), 'w') as f:
    json.dump(all_results, f, indent=4)
        