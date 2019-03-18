def construct_new_dataset(datasets, stats, max_samples_per_set, test_set_size):
    import numpy as np    
    from copy import deepcopy

    print("Constructing new dataset..")

    if max_samples_per_set is None:
        max_samples_per_set = min(stats, key=lambda x: x['total'])['total']

    num_per_label = max_samples_per_set // 3
    
    dataset_names = datasets.keys()

    dataset_dict = {dname:list() for dname in dataset_names}

    train_set = deepcopy(dataset_dict)
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

            sub_set = label_set[:num_per_label] + label_set[num_per_label: num_per_label + left_over]
            train_test_split = int(len(sub_set) * (1-test_set_size))

            train_set[dname] += sub_set[:train_test_split]
            test_set[dname] += sub_set[train_test_split:]

            left_over += num_per_label - len(sub_set)