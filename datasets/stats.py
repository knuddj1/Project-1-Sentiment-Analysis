import os
from .settings import *


def save_stats(dataset_stats, save_file):
    with open(save_file, "w") as f:
        f.writelines(dataset_stats)



def prepare_stats(stats):
    stats = gather_stats(datasets)

    counts_converter = {-1: "negative", 0: "neutral", 1: "positive"}

    dataset_stats = ""

    dataset_stats += "Average input length = {} characters \n".format(avg_len)
    dataset_stats += "Min input length = {} characters \n".format(min_len)
    dataset_stats += "Max input length = {} characters \n".format(max_len)
    dataset_stats += "\n"
    for k, v in label_counts.items():
        dataset_stats += "Total {} samples: {} \n".format(counts_converter[k], v)

    save_stats(dataset_stats, save_file)
    print(total_counts)
    print(global_avg / len(sub_sets))

    save_stats()


def gather_stats(datasets):
    sub_sets = datasets.keys()

    total_counts = {-1: 0, 0: 0, 1: 0}
    global_avg = 0

    if STATS_SAVE_DIR is None:
        save_dir = os.path.dirname(__file__)
    save_dir = os.path.join(save_dir, "dataset_stats")
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    else:
        save_dir = STATS_SAVE_DIR

    for dname in sub_sets:
        save_file = os.path.join(save_dir, dname + ".txt")

        # If dataset already has summary skip it
        if os.path.exists(save_file):
            continue

        label_counts = {-1: 0, 0: 0, 1: 0}
        min_len = len(datasets[dname])  # big number for initial value
        max_len = 0
        total_lens = 0

        for sample in datasets[dname]:
            label_counts[sample["label"]] += 1
            sample_len = len(sample["input"])
            total_lens += sample_len
            if sample_len < min_len:
                min_len = sample_len
            elif sample_len > max_len:
                max_len = sample_len

        avg_len = total_lens // len(datasets[dname])

        for k, v in label_counts.items():
            total_counts[k] += v

        global_avg += avg_len

        prepare_stats(stats)


