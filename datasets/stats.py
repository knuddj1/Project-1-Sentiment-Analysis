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
        "negative samples": len([None for i in labels if i == -1]),
        "neutral samples": len([None for i in labels if i == 0]),
        "positive samples": len([None for i in labels if i == 1]),
        "total samples": len(dataset),
        "min sample length": lens[0],
        "max sample length": lens[-1],
        "samples length arithmetic mean": statistics.mean(lens),
        "samples length harmonic_mean": statistics.harmonic_mean(lens),
        "median sample length": statistics.median(lens),
        "sample lengths mode": statistics.mode(lens),
        "sample lengths stdev": statistics.stdev(lens),
        "sample lengths variance": statistics.variance(lens)

    }


def generate_stats(datasets):
    print("Generating statistics for dataset..")

    save_file = "dataset statistics.csv"
    subset_names = datasets.keys()

    dataset_stats = [gather_dataset_stats(datasets[dname], dname) for dname in subset_names]
    save_stats(dataset_stats, save_file)

    print("Finished! Statistics saved as '%s'" % save_file)





