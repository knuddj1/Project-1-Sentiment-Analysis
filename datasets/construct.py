import csv
import json


def get_subset(datasets, test_set_size):
    """"
    datasets : dict - single/multiple dataset in format {"dataset_name":{"input":x,"label":x}}
    --------------------------------------------------------------------
    output : dict -> train_set - subset of each dataset concatenated
                                 size = subset * (1 - test_size)
             dict -> test_set - subset of each dataset concatenated
                                 size = subset * test_size
    --------------------------------------------------------------------
    TODO
    """
    import numpy as np    
    from copy import deepcopy

    max_samples_per_set = len(min(datasets.items(), key=lambda k_v: len(k_v[1]))[1])

    num_per_label = max_samples_per_set // 3
    
    dataset_dict = {dname:list() for dname in datasets.keys()}

    train_set = list()
    test_set = deepcopy(dataset_dict)

    datasets_by_labels = {
        label:deepcopy(dataset_dict) for label in [-1,0,1]
    }

    for idx, (dname, dataset) in enumerate(datasets.items()):
        for s in dataset: datasets_by_labels[s['label']][dname].append(s)

    for label, data in datasets_by_labels.items():

        left_over = 0 
        data = sorted(data.items(), key=lambda k_v: len(k_v[1]))

        for dname, label_set in data:
            np.random.shuffle(dataset)

            subset = label_set[:num_per_label]
            extra = label_set[num_per_label: num_per_label + left_over]
            final = subset + extra

            train_test_split = int(len(final) * (1-test_set_size))

            train_set += final[:train_test_split]
            test_set[dname] += final[train_test_split:]

            left_over += num_per_label - len(final)

    return train_set, test_set