def save_stats(dataset_stats, save_file):
    with open(save_file, "w") as f:
        f.writelines(dataset_stats)



# def prepare_stats(stats):
#     counts_converter = {-1: "negative", 0: "neutral", 1: "positive"}
#
#     dataset_stats = ""
#
#     dataset_stats += "Average input length = {} characters \n".format(avg_len)
#     dataset_stats += "Min input length = {} characters \n".format(min_len)
#     dataset_stats += "Max input length = {} characters \n".format(max_len)
#     dataset_stats += "\n"
#     for k, v in label_counts.items():
#         dataset_stats += "Total {} samples: {} \n".format(counts_converter[k], v)
#
#     save_stats(dataset_stats, save_file)
#     print(total_counts)
#     print(global_avg / len(sub_sets))


def gather_dataset_stats(dataset):

    lens = [len(s["input"]) for s in dataset]
    labels = [s["label"] for s in dataset]

    return {
        "n_neg": len([None for i in labels if i == -1]),
        "n_neut": len([None for i in labels if i == 0]),
        "n_pos": len([None for i in labels if i == 1]),
        "min_len": min(lens),
        "max_len": max(lens),
        "avg_len": sum(lens) // len(dataset)
    }


def generate_stats(datasets):
    sub_sets = datasets.keys()

    total_counts = {-1: 0, 0: 0, 1: 0}
    global_avg = 0

    dataset_stats = dict.fromkeys(sub_sets)

    for dname in sub_sets:
        dataset_stats[dname] = gather_dataset_stats(datasets[dname])

    import json
    with open("test.json", "w") as f:
        json.dump(dataset_stats, f, indent=4)






