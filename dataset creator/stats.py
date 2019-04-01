import statistics
import csv


def gather_dataset_stats(dataset, dataset_name):
    """"
    dataset : dict - singular dataset in format {"input":x,"label":x}
    --------------------------------------------------------------------
    output : dict - statistics of dataset
    --------------------------------------------------------------------
    calculates statistics for a given dataset
    """
    lens = sorted([len(s["input"]) for s in dataset])
    labels = [s["label"] for s in dataset]

    return {
        "dataset": dataset_name,
        "negative": len([None for i in labels if i == -1]),
        "neutral": len([None for i in labels if i == 0]),
        "positive": len([None for i in labels if i == 1]),
        "total": len(dataset),
        "min_length": lens[0],
        "max_length": lens[-1],
        "arithmetic_mean": statistics.mean(lens),
        "harmonic_mean": statistics.harmonic_mean(lens),
        "median": statistics.median(lens),
        "mode": statistics.mode(lens),
        "stdev": statistics.stdev(lens),
        "variance": statistics.variance(lens)
    }


def generate_stats(datasets):
    """"
    datasets : dict - single/multiple dataset in format {"dataset_name":{"input":x,"label":x}}
    --------------------------------------------------------------------
    output : list(dict) - statistics of dataset
    --------------------------------------------------------------------
    calculates statistics for all datasets and save them to a csv file.
    """
    
    # Gather statistics on each dataset
    return [gather_dataset_stats(subset, dname) for dname, subset in datasets.items()]