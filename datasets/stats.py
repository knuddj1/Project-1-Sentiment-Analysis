import statistics
import csv


def save_stats(dataset_stats, save_file):
    """"
    dataset_stats : list(dict) - Each list item is a dict of all dataset statistics
    save_file : string - location to save dataset_stats
    --------------------------------------------------------------------
    saves dataset statistics to a csv file
    """

    with open(save_file, mode="w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=dataset_stats[0].keys())
        writer.writeheader()
        writer.writerows(dataset_stats)


def gather_dataset_stats(dataset, dataset_name):
    """"
    dataset : dict - singular dataset in format {"input":x,"label":x}
    --------------------------------------------------------------------
    output : dict - statistics of dataset
    --------------------------------------------------------------------
    TODO
    """
    lens = sorted([len(s["input"]) for s in dataset])
    labels = [s["label"] for s in dataset]

    return {
        "dataset": dataset_name,
        "negative": len([None for i in labels if i == -1]),
        "neutral": len([None for i in labels if i == 0]),
        "positive": len([None for i in labels if i == 1]),
        "total": len(dataset),
        "min length": lens[0],
        "max length": lens[-1],
        "arithmetic mean": statistics.mean(lens),
        "harmonic_mean": statistics.harmonic_mean(lens),
        "median": statistics.median(lens),
        "mode": statistics.mode(lens),
        "stdev": statistics.stdev(lens),
        "variance": statistics.variance(lens)

    }


def generate_stats(datasets):
    print("Generating statistics for dataset..")

    save_file = "dataset statistics.csv"

    # Gather statistics on each dataset
    dataset_stats = [gather_dataset_stats(subset, dname) for dname, subset in datasets.items()]

    # Export statistics to csv file
    save_stats(dataset_stats, save_file)

    print("Finished! Statistics saved as '%s'" % save_file)





