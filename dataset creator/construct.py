import csv
import json
import numpy as np 


def equal(datasets, test_set_size, shuffle, n_shuffles):
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
            if shuffle:
                for _ in range(n_shuffles):
                    np.random.shuffle(label_set)

            subset = label_set[:num_per_label]
            extra = label_set[num_per_label: num_per_label + left_over]
            final = subset + extra

            train_test_split = int(len(final) * (1-test_set_size))

            train_set += final[:train_test_split]
            test_set[dname] += final[train_test_split:]

            left_over += num_per_label - len(final)

    return train_set, test_set


def percentage(datasets, test_set_size, configs, shuffle, n_shuffles):
    train_set = list()
    test_set = {dname:list() for dname in datasets.keys()}

    for dname, data in datasets.items():
        keep_percent = int(len(data) // configs[dname]["PERCENT"])
        train_test_split = int(keep_percent * (1-test_set_size))
        if shuffle:
            for _ in range(n_shuffles):
                np.random.shuffle(data)
        subset = data[:keep_percent]
        train_set += subset[:train_test_split]
        test_set[dname] = subset[train_test_split:]
    return train_set, test_set


def get_subset(datasets, settings):
    if settings["CONCAT_TYPE"] == "equal":
        return equal(
            datasets,
            settings["TEST_SET_SIZE"],
            settings["SHUFFLE"],
            settings["NUM_SHUFFLES"]
        )
    elif settings["CONCAT_TYPE"] == "percentage":
        return percentage(
            datasets,
            settings["TEST_SET_SIZE"],
            settings["CONFIGS"],
            settings["SHUFFLE"],
            settings["NUM_SHUFFLES"]
        )